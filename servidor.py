import socket
import os
import random
import time

HOST = "127.0.0.1" #este computador
PORTA = 5000
TAMANHO_BUFFER = 2048 #1024x2 (folga)
TAMANHO_BLOCO = 1024
PASTA_DESTINO = "arquivos_servidor" #onde os arquivos recebidos serão salvos

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
        
#cria a pasta de destino, caso não exista
os.makedirs(PASTA_DESTINO, exist_ok=True) 

#criação do socket UDP
#AF_INET - endereço IPv4
#SOCK_DGRAM - UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#associa o socket ao endereço e a porta
sock.bind((HOST,PORTA))

print(f"[SERVIDOR] escutando em {HOST}:{PORTA}...") #sinaliza que o servidor está ativo

nome_arquivo_atual = None
blocos = []
esperado = 0 #proximo seq
try:
    while True: #mantem o servidor sempre ligado
        #espera a chegada de algum pacote, se não chega ele fica travado esperando
        dados, endereco, esperado = rdt_receber(sock, esperado)

        if dados.startswith(b"INICIO|"):   #em cliente.py o primeiro pacote do arquivo é enviado com "INICIO|" -> identifica a chegada de um novo arquivo
            nome_arquivo_atual = dados.decode().split("|",1)[1]
            blocos = [] #zera a lista para um novo arquivo
            print(f"[SERVIDOR] Início do arquivo '{nome_arquivo_atual}' vindo de {endereco}") #sinaliza nome do arquivo e o endereço que veio
        elif dados == b"FIM": #chegou ao fim do arquivo
            #junta todos os pedaços em uma sequência única de bytes
            conteudo_completo = b"".join(blocos)

            #salva com o prefixo "servidor_"
            nome_salvar = f"servidor_{nome_arquivo_atual}"
            caminho_salvar = os.path.join(PASTA_DESTINO, nome_salvar) #salva na pasta "arquivos_servidor" o arquivo de destino de todos os pacotes(blocos)

            with open(caminho_salvar, "wb") as f:
                f.write(conteudo_completo) #escreve todo o conteudo no arquivo

            print(f"[SERVIDOR] Arquivo salvo como '{caminho_salvar}'" 
                  f"({len(conteudo_completo)} bytes, {len(blocos)} pacotes)")

            #quando termina de receber e salva o arquivo, inicia o envio para o cliente
            print(f"[SERVIDOR] Devolvendo {nome_arquivo_atual} para {endereco}...") #endereço do cliente, de onde veio os dados
            seq = 0
            seq = rdt_enviar(sock, endereco, f"INICIO|{nome_arquivo_atual}".encode(), seq, reack=True)
            numero_envio = 0
            for i in range(0, len(conteudo_completo), TAMANHO_BLOCO):  #devolução de cada pedaço do arquivo respeitando o limite de 1024 bytes
                bloco = conteudo_completo[i:i + TAMANHO_BLOCO]
                numero_envio += 1
                print(f"[SERVIDOR] Pacote {numero_envio} devolvido ({len(bloco)} bytes)")
                seq = rdt_enviar(sock, endereco, bloco, seq, reack=True)

            seq = rdt_enviar(sock, endereco, b"FIM", seq, reack=True) #quando sai do for envia o "FIM" para avisar que o arquivo terminou
            print(f"[SERVIDOR] Devolução concluída: {numero_envio} pacotes.")
            esperado = 0


        else:  #ainda está recebendo blocos do arquivo
            blocos.append(dados) #adiciona o pedaço na lista de blocos
            print(f"[SERVIDOR] Pacote {len(blocos)} recebido ({len(dados)} bytes)")


except KeyboardInterrupt:
    print("\n[SERVIDOR] Encerrado pelo usuário")
finally:
    sock.close()
