import socket
import os

HOST = "127.0.0.1" #este computador
PORTA = 5000
TAMANHO_BUFFER = 2048 #1024x2 (folga)
TAMANHO_BLOCO = 1024
PASTA_DESTINO = "arquivos_servidor" #onde os arquivos recebidos serão salvos

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
try:
    while True: #mantem o servidor sempre ligado
        #espera a chegada de algum pacote, se não chega ele fica travado esperando
        dados, endereco = sock.recvfrom(TAMANHO_BUFFER)

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
            sock.sendto(f"INICIO|{nome_arquivo_atual}".encode(), endereco) #envia com a identificaçaõ "INICIO|" para o endereço do cliente
            numero_envio = 0
            for i in range(0, len(conteudo_completo), TAMANHO_BLOCO):  #devolução de cada pedaço do arquivo respeitando o limite de 1024 bytes
                bloco = conteudo_completo[i:i + TAMANHO_BLOCO]
                sock.sendto(bloco, endereco)
                numero_envio += 1
                print(f"[SERVIDOR] Pacote {numero_envio} devolvido ({len(bloco)} bytes)")

            sock.sendto(b"FIM", endereco) #quando sai do for envia o "FIM" para avisar que o arquivo terminou
            print(f"[SERVIDOR] Devolução concluída: {numero_envio} pacotes.")


        else:  #ainda está recebendo blocos do arquivo
            blocos.append(dados) #adiciona o pedaço na lista de blocos
            print(f"[SERVIDOR] Pacote {len(blocos)} recebido ({len(dados)} bytes)")


except KeyboardInterrupt:
    print("\n[SERVIDOR] Encerrado pelo usuário")
finally:
    sock.close()
