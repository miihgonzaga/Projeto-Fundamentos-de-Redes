import socket
import sys #leitura de parâmetros no terminal
import os #lida com arquivos e caminhos
import random
import time

HOST = "127.0.0.1"
PORTA = 5000
TAMANHO_PCT = 1024
TAMANHO_BUFFER = 2048
PASTA_DESTINO = "arquivos_cliente" #pasta para guardar arquivos recebidos do servidor

TIMEOUT = 1.0 #segundos
PROBABILIDADE_PERDA = 0.3
PROBABILIDADE_CORRUPCAO = 0.1
DADOS, ACK, NAK = 0, 1, 2

#as funcoes de rdt estarao nos dois arquivos ao invés de fazer um arquivo rdt.py so pra implementar rdt

CAB_TAM = 4   # tipo (1B) + seq (1B) + checksum (2B)

def checksum(dados):
    soma = 0
    for b in dados:
        soma = (soma * 31 + b) & 0xFFFF#mantém em 16 bits
    return soma

def montar_pkt(tipo, seq, payload=b""):#monta pacote
    check = checksum(bytes([tipo, seq]) + payload)
    return bytes([tipo, seq]) + check.to_bytes(2, "big") + payload

def desmontar_pkt(pacote): #desmonta o pacote
    if len(pacote) < CAB_TAM:
        return None
    tipo, seq = pacote[0], pacote[1]
    check = int.from_bytes(pacote[2:4], "big")
    payload = pacote[4:]
    if check != checksum(bytes([tipo, seq]) + payload):
        return None
    return tipo, seq, payload

def enviar_udp(sock, pacote, destino, rotulo): #pode perder ou corromper o pacote.
    if random.random() < PROBABILIDADE_PERDA:
        print(f"[CANAL] {rotulo} PERDIDO")
        return
    if random.random() < PROBABILIDADE_CORRUPCAO:
        b = bytearray(pacote)
        b[-1] ^= 0xFF
        pacote = bytes(b)
        print(f"[CANAL] {rotulo} CORROMPIDO")
    sock.sendto(pacote, destino)

def rdt_enviar(sock, destino, payload, seq, reack=False): #stop-and-wait. Retorna o proximo seq
    pacote = montar_pkt(DADOS, seq, payload)
    retransmissoes = 0
    while True:
        print(f"[RDT] Enviando DADOS seq={seq} ({len(payload)} bytes)"
              + (f"[retransmissão {retransmissoes}]" if retransmissoes else ""))
        enviar_udp(sock, pacote, destino, f"DADOS seq={seq}")
        fim_timer = time.time() + TIMEOUT
        while True:
            restante = fim_timer - time.time()
            if restante <= 0:
                print(f"[RDT] TIMEOUT seq={seq} -> retransmitindo")
                break
            sock.settimeout(restante)
            try:
                dados, end = sock.recvfrom(TAMANHO_BUFFER)
            except socket.timeout:
                print(f"[RDT] TIMEOUT seq={seq} -> retransmitindo")
                break
            except ConnectionResetError:   # Windows: porta do outro lado fechada
                continue
            r = desmontar_pkt(dados)
            if r is None:
                print("[RDT] Resposta corrompida, ignorando")
                continue
            tipo, s, p = r
            if tipo == ACK and s == seq:
                print(f"[RDT] ACK {seq} recebido")
                return 1 - seq
            if tipo == NAK:
                print("[RDT] NAK recebido -> retransmitindo")
                break
            if tipo == DADOS and reack:
                print(f"[RDT] DADOS duplicado seq={s} durante espera -> reenviando ACK {s}")
                enviar_udp(sock, montar_pkt(ACK, s), end, f"ACK {s}")
                continue
            print(f"[RDT] Pacote inesperado (tipo={tipo}, seq={s}), ignorando")
        retransmissoes += 1

def rdt_receber(sock, esperado): #Retorna (payload, endereco, proximo_esperado)
    sock.settimeout(None)
    while True:
        try:
            dados, end = sock.recvfrom(TAMANHO_BUFFER)
        except ConnectionResetError:
            continue
        r = desmontar_pkt(dados)
        if r is None:
            print("[RDT] Pacote corrompido -> enviando NAK")
            enviar_udp(sock, montar_pkt(NAK, 1 - esperado), end, "NAK")
            continue
        tipo, seq, payload = r
        if tipo != DADOS:
            continue
        if seq == esperado:
            print(f"[RDT] DADOS seq={seq} OK -> enviando ACK {seq}")
            enviar_udp(sock, montar_pkt(ACK, seq), end, f"ACK {seq}")
            return payload, end, 1 - esperado
        print(f"[RDT] Duplicata seq={seq} (esperava {esperado}) -> reenviando ACK {seq}")
        enviar_udp(sock, montar_pkt(ACK, seq), end, f"ACK {seq}")

#lê o nome do arquivo digitado no terminal ("python cliente.py texte.txt")
#o sys.argv gera uma lista com tudo que foi escrito no terminal
if len(sys.argv) != 2: #se o tamanho da lista ta diferente de 2 você esqueceu algo
    print("Uso: python cliente.py <arquivos_teste/nome_do_arquivo>") #com essa formatação -> sys.argv[1] = <nome_do_arquivo>
    sys.exit(1)

caminho = sys.argv[1]  #assimila o caminho ao nome do arquivo escrito no terminal


#verifica se o arquivo existe
if not os.path.isfile(caminho):
    print(f"[CLIENTE] Arquivo '{caminho}' não encontrado")
    sys.exit(1)

nome_arquivo = os.path.basename(caminho)  #pega o nome do arquivo
os.makedirs(PASTA_DESTINO, exist_ok=True) #cria a pasta destino

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #estabelece conexão

#Primeio pacote informa o nome e indica que o que chega agora faz parte desse pacote
print(f"[CLIENTE] Enviando arquivo '{nome_arquivo}'...")

#Pacotes de dados (blocos de até 1024 bytes)
numero = 0
seq = 0
seq = rdt_enviar(sock, (HOST, PORTA), f"INICIO|{nome_arquivo}".encode(), seq)
with open (caminho, "rb") as f:  #abre o arquivo em read binary (rb)
    while True:
        bloco = f.read(TAMANHO_PCT) #lê até 1024 bytes por vez
        if not bloco:
            break
        seq = rdt_enviar(sock, (HOST, PORTA), bloco, seq)#envia o bloco para o servidor
        numero +=1
        print(f"[CLIENTE] Pacote {numero} enviado ({len(bloco)} bytes)")

#Último pacote, encerra o recebimento desse pacote
seq = rdt_enviar(sock, (HOST, PORTA), b"FIM", seq)
print(f"[CLIENTE] Envio concluído: {numero} pacotes.")

# devolução: agora o cliente é o receptor
esperado = 0
while True:
    dados, endereco, esperado = rdt_receber(sock, esperado) #recebe o pacote, respeitando o tamanho do buffer

    if dados.startswith(b"INICIO|"): #verifica se é o início do arquivo (faz o mesmo processo que é feito no "servidor.py")
        nome_recebido = dados.decode().split("|", 1)[1]
        blocos_recebidos = []
        print(f"[CLIENTE] Recebendo devolução do arquivo '{nome_recebido}'...")

    elif dados == b"FIM":
        conteudo_completo = b"".join(blocos_recebidos)
        nome_salvar = f"cliente_{nome_recebido}"
        caminho_salvar = os.path.join(PASTA_DESTINO, nome_salvar)

        with open(caminho_salvar, "wb") as f:
            f.write(conteudo_completo)

        print(f"[CLIENTE] Arquivo salvo como '{caminho_salvar}' "
              f"({len(conteudo_completo)} bytes, {len(blocos_recebidos)} pacotes)")
        break  #terminou, pode sair do loop

    else:
        blocos_recebidos.append(dados)
        print(f"[CLIENTE] Pacote {len(blocos_recebidos)} recebido ({len(dados)} bytes)")

#caso o ACK do fim tenha se perdido, o cliente vai reenviando ACKs de duplicatadas por um tempo
print("[CLIENTE] Aguardando em caso de retransmissão do FIM pelo servidor...")
while True:
    sock.settimeout(3 * TIMEOUT)
    try:
        dados, end = sock.recvfrom(TAMANHO_BUFFER)
    except socket.timeout:
        break
    except ConnectionResetError:
        continue
    r = desmontar_pkt(dados)
    if r is not None and r[0] == DADOS:
        print(f"[RDT] Duplicata seq={r[1]} após o fim -> reenviando ACK {r[1]}")
        enviar_udp(sock, montar_pkt(ACK, r[1]), end, f"ACK {r[1]}")
 
print("[CLIENTE] Encerrado.")

sock.close()
