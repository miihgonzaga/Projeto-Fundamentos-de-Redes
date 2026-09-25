import socket
import sys #leitura de parâmetros no terminal
import os #lida com arquivos e caminhos

HOST = "127.0.0.1"
PORTA = 5000
TAMANHO_PCT = 1024
TAMANHO_BUFFER = 2048
PASTA_DESTINO = "arquivos_cliente" #pasta para guardar arquivos recebidos do servidor


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
sock.sendto(f"INICIO|{nome_arquivo}".encode(), (HOST,PORTA)) #o encode converte o texto em bytes
print(f"[CLIENTE] Enviando arquivo '{nome_arquivo}'...")

#Pacotes de dados (blocos de até 1024 bytes)
numero = 0
with open (caminho, "rb") as f:  #abre o arquivo em read binary (rb)
    while True:
        bloco = f.read(TAMANHO_PCT) #lê até 1024 bytes por vez
        if not bloco:
            break
        sock.sendto(bloco, (HOST,PORTA)) #envia o bloco para o servidor
        numero +=1
        print(f"[CLIENTE] Pacote {numero} enviado ({len(bloco)} bytes)")

#Último pacote, encerra o recebimento desse pacote
sock.sendto(b"FIM", (HOST,PORTA))
print(f"[CLIENTE] Envio concluído: {numero} pacotes.")


#inicia o recebimento do pacote
print("[CLIENTE] Aguardando devolução do servidor...")

nome_recebido = None
blocos_recebidos = []

while True:
    dados, endereco = sock.recvfrom(TAMANHO_BUFFER) #recebe o pacote, respeitando o tamanho do buffer

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
        break  # terminou, pode sair do loop

    else:
        blocos_recebidos.append(dados)
        print(f"[CLIENTE] Pacote {len(blocos_recebidos)} recebido ({len(dados)} bytes)")

sock.close()

