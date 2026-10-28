# Projeto de Redes 2026.2 - Parte 1

**Universidade Federal de Pernambuco - UFPE**

**CIN 0018 - Fundamentos de Redes de Computadores**

**Docente:** Renato Mariz de Moraes

**Equipe 1 - Integrantes:** Miriam Gonzaga da Silva Santos, Maria Gabriella Medeiros da Silva, Lucas Jose Duarte Cavalcanti e Mario Daniel Teles da Silva Filho

# Transferência Confiável Segundo o Canal de Transmissão RDT3.0

Esta parte do projeto implementa uma aplicação cliente-servidor através de transferência de arquivos via **Canal de Transmissão RDT3.0** na linguagem Python, utilizando as bibliotecas socket, sys e os. 

Arquivos enviados do cliente são armazenados com o prefixo “servidor_” e devolvidos ao cliente com o prefixo “cliente_”. 

## Estrutura

- cliente.py (Arquivo python com o código do cliente RDT3.0)
- servidor.py (Arquivo python com o código do servidor RDT3.0)
- arquivos_teste  (Pasta de arquivos usados nos testes - formato txt e jpeg)
- arquivos_cliente (Pasta de arquivos devolvidos pelo servidor - prefixo “cliente_” e formato txt e jpg)
- arquivos_servidor (Pasta de arquivos recebidos e salvos pelo servidor - prefixo “servidor_” e formato txt e jpg)

## Como Executar

### Passo 1

Abrir dois terminais na pasta do projeto; 

### Passo 2

No primeiro terminal, inicie o servidor com o comando `python servidor.py`

Exemplo de saída esperada: `[SERVIDOR] escutando em 127.0.0.1:5000...`

### Passo 3

No segundo terminal, envie um arquivo do formato txt com o comando  `python cliente.py arquivos_teste/texto1.txt`  

Exemplo de saída esperada no terminal cliente: 

```
[CLIENTE] Enviando arquivo 'texto1.txt'...
[RDT] Enviando DADOS seq=0 (17 bytes)
[CANAL] DADOS seq=0 PERDIDO
[RDT] TIMEOUT seq=0 -> retransmitindo
[RDT] Enviando DADOS seq=0 (17 bytes)[retransmissão 1]
[CANAL] DADOS seq=0 PERDIDO
[RDT] TIMEOUT seq=0 -> retransmitindo
[RDT] Enviando DADOS seq=0 (17 bytes)[retransmissão 2]
[CANAL] DADOS seq=0 PERDIDO
[RDT] TIMEOUT seq=0 -> retransmitindo
[RDT] Enviando DADOS seq=0 (17 bytes)[retransmissão 3]
[CANAL] DADOS seq=0 PERDIDO
[RDT] TIMEOUT seq=0 -> retransmitindo
[RDT] Enviando DADOS seq=0 (17 bytes)[retransmissão 4]
[RDT] ACK 0 recebido
[RDT] Enviando DADOS seq=1 (519 bytes)
[RDT] ACK 1 recebido
[CLIENTE] Pacote 1 enviado (519 bytes)
[RDT] Enviando DADOS seq=0 (3 bytes)
[RDT] ACK 0 recebido
[CLIENTE] Envio concluído: 1 pacotes.
[RDT] Pacote corrompido -> enviando NAK
[CANAL] NAK PERDIDO
[RDT] DADOS seq=0 OK -> enviando ACK 0
[CANAL] ACK 0 PERDIDO
[CLIENTE] Recebendo devolução do arquivo 'texto1.txt'...
[RDT] Duplicata seq=0 (esperava 1) -> reenviando ACK 0
[RDT] DADOS seq=1 OK -> enviando ACK 1
[CLIENTE] Pacote 1 recebido (519 bytes)
[RDT] DADOS seq=0 OK -> enviando ACK 0
[CLIENTE] Arquivo salvo como 'arquivos_cliente\cliente_texto1.txt' (519 bytes, 1 pacotes)
[CLIENTE] Aguardando em caso de retransmissão do FIM pelo servidor...
[CLIENTE] Encerrado.
```
Exemplo de saída esperada no terminal servidor:

```
[RDT] DADOS seq=0 OK -> enviando ACK 0
[SERVIDOR] Início do arquivo 'texto1.txt' vindo de ('127.0.0.1', 64377)
[RDT] DADOS seq=1 OK -> enviando ACK 1
[SERVIDOR] Pacote 1 recebido (519 bytes)
[RDT] DADOS seq=0 OK -> enviando ACK 0
[CANAL] ACK 0 PERDIDO
[SERVIDOR] Arquivo salvo como 'arquivos_servidor\servidor_texto1.txt'(519 bytes, 1 pacotes)
[SERVIDOR] Devolvendo texto1.txt para ('127.0.0.1', 64377)...
[RDT] Enviando DADOS seq=0 (17 bytes)
[CANAL] DADOS seq=0 PERDIDO
[RDT] DADOS duplicado seq=0 durante espera -> reenviando ACK 0
[RDT] TIMEOUT seq=0 -> retransmitindo
[RDT] Enviando DADOS seq=0 (17 bytes)[retransmissão 1]
[CANAL] DADOS seq=0 PERDIDO
[RDT] TIMEOUT seq=0 -> retransmitindo
[RDT] Enviando DADOS seq=0 (17 bytes)[retransmissão 2]
[CANAL] DADOS seq=0 PERDIDO
[RDT] TIMEOUT seq=0 -> retransmitindo
[RDT] Enviando DADOS seq=0 (17 bytes)[retransmissão 3]
[RDT] ACK 0 recebido
[SERVIDOR] Pacote 1 devolvido (519 bytes)
[RDT] Enviando DADOS seq=1 (519 bytes)
[RDT] TIMEOUT seq=1 -> retransmitindo
[RDT] Enviando DADOS seq=1 (519 bytes)[retransmissão 1]
[CANAL] DADOS seq=1 PERDIDO
[RDT] TIMEOUT seq=1 -> retransmitindo
[RDT] Enviando DADOS seq=1 (519 bytes)[retransmissão 2]
[RDT] Resposta corrompida, ignorando
[RDT] TIMEOUT seq=1 -> retransmitindo
[RDT] Enviando DADOS seq=1 (519 bytes)[retransmissão 3]
[CANAL] DADOS seq=1 PERDIDO
[RDT] TIMEOUT seq=1 -> retransmitindo
[RDT] Enviando DADOS seq=1 (519 bytes)[retransmissão 4]
[CANAL] DADOS seq=1 PERDIDO
[RDT] TIMEOUT seq=1 -> retransmitindo
[RDT] Enviando DADOS seq=1 (519 bytes)[retransmissão 5]
[RDT] TIMEOUT seq=1 -> retransmitindo
[RDT] Enviando DADOS seq=1 (519 bytes)[retransmissão 6]
[CANAL] DADOS seq=1 PERDIDO
[RDT] TIMEOUT seq=1 -> retransmitindo
[RDT] Enviando DADOS seq=1 (519 bytes)[retransmissão 7]
[RDT] ACK 1 recebido
[RDT] Enviando DADOS seq=0 (3 bytes)
[CANAL] DADOS seq=0 PERDIDO
[RDT] TIMEOUT seq=0 -> retransmitindo
[RDT] Enviando DADOS seq=0 (3 bytes)[retransmissão 1]
[RDT] ACK 0 recebido
[SERVIDOR] Devolução concluída: 1 pacotes.
```

Envie um arquivo do formato jpeg com o comando `python cliente.py arquivos_teste/imagem1.jpg`

Exemplo de saída esperada no terminal cliente: 

```
[CLIENTE] Enviando arquivo 'imagem1.jpg'...
[RDT] Enviando DADOS seq=0 (18 bytes)
[RDT] ACK 0 recebido
[RDT] Enviando DADOS seq=1 (1024 bytes)
[RDT] ACK 1 recebido
[CLIENTE] Pacote 1 enviado (1024 bytes)
[RDT] Enviando DADOS seq=0 (1024 bytes)
[RDT] ACK 0 recebido
[CLIENTE] Pacote 2 enviado (1024 bytes)
[RDT] Enviando DADOS seq=1 (1024 bytes)
[CANAL] DADOS seq=1 CORROMPIDO
[RDT] Resposta corrompida, ignorando
[RDT] TIMEOUT seq=1 -> retransmitindo
[RDT] Enviando DADOS seq=1 (1024 bytes)[retransmissão 1]
[RDT] ACK 1 recebido
[CLIENTE] Pacote 3 enviado (1024 bytes)
[RDT] Enviando DADOS seq=0 (1024 bytes)
[CANAL] DADOS seq=0 PERDIDO
[RDT] TIMEOUT seq=0 -> retransmitindo
[RDT] Enviando DADOS seq=0 (1024 bytes)[retransmissão 1]
[CANAL] DADOS seq=0 PERDIDO
[RDT] TIMEOUT seq=0 -> retransmitindo
[RDT] Enviando DADOS seq=0 (1024 bytes)[retransmissão 2]
[CANAL] DADOS seq=0 PERDIDO
[RDT] TIMEOUT seq=0 -> retransmitindo
[RDT] Enviando DADOS seq=0 (1024 bytes)[retransmissão 3]
[RDT] ACK 0 recebido
[CLIENTE] Pacote 4 enviado (1024 bytes)
[RDT] Enviando DADOS seq=1 (1024 bytes)
[RDT] ACK 1 recebido
[CLIENTE] Pacote 5 enviado (1024 bytes)
[RDT] Enviando DADOS seq=0 (1024 bytes)
[RDT] TIMEOUT seq=0 -> retransmitindo
[RDT] Enviando DADOS seq=0 (1024 bytes)[retransmissão 1]
[CANAL] DADOS seq=0 PERDIDO
[RDT] TIMEOUT seq=0 -> retransmitindo
[RDT] Enviando DADOS seq=0 (1024 bytes)[retransmissão 2]
[RDT] ACK 0 recebido
[CLIENTE] Pacote 6 enviado (1024 bytes)
[RDT] Enviando DADOS seq=1 (1024 bytes)
[RDT] ACK 1 recebido
[CLIENTE] Pacote 7 enviado (1024 bytes)
[RDT] Enviando DADOS seq=0 (1024 bytes)
[CANAL] DADOS seq=0 PERDIDO
[RDT] TIMEOUT seq=0 -> retransmitindo
[RDT] Enviando DADOS seq=0 (1024 bytes)[retransmissão 1]
[CANAL] DADOS seq=0 PERDIDO
[RDT] TIMEOUT seq=0 -> retransmitindo
[RDT] Enviando DADOS seq=0 (1024 bytes)[retransmissão 2]
[RDT] ACK 0 recebido
[CLIENTE] Pacote 8 enviado (1024 bytes)
[RDT] Enviando DADOS seq=1 (1024 bytes)
[CANAL] DADOS seq=1 PERDIDO
[RDT] TIMEOUT seq=1 -> retransmitindo
[RDT] Enviando DADOS seq=1 (1024 bytes)[retransmissão 1]
[RDT] TIMEOUT seq=1 -> retransmitindo
[RDT] Enviando DADOS seq=1 (1024 bytes)[retransmissão 2]
[RDT] ACK 1 recebido
[CLIENTE] Pacote 9 enviado (1024 bytes)
[RDT] Enviando DADOS seq=0 (1024 bytes)
[RDT] ACK 0 recebido
[CLIENTE] Pacote 10 enviado (1024 bytes)
[RDT] Enviando DADOS seq=1 (1024 bytes)
[CANAL] DADOS seq=1 PERDIDO
[RDT] TIMEOUT seq=1 -> retransmitindo
[RDT] Enviando DADOS seq=1 (1024 bytes)[retransmissão 1]
[RDT] ACK 1 recebido
[CLIENTE] Pacote 11 enviado (1024 bytes)
[RDT] Enviando DADOS seq=0 (471 bytes)
[RDT] ACK 0 recebido
[CLIENTE] Pacote 12 enviado (471 bytes)
[RDT] Enviando DADOS seq=1 (3 bytes)
[RDT] ACK 1 recebido
[CLIENTE] Envio concluído: 12 pacotes.
[RDT] DADOS seq=0 OK -> enviando ACK 0
[CANAL] ACK 0 CORROMPIDO
[CLIENTE] Recebendo devolução do arquivo 'imagem1.jpg'...
[RDT] Duplicata seq=0 (esperava 1) -> reenviando ACK 0
[RDT] DADOS seq=1 OK -> enviando ACK 1
[CLIENTE] Pacote 1 recebido (1024 bytes)
[RDT] DADOS seq=0 OK -> enviando ACK 0
[CLIENTE] Pacote 2 recebido (1024 bytes)
[RDT] Pacote corrompido -> enviando NAK
[RDT] DADOS seq=1 OK -> enviando ACK 1
[CLIENTE] Pacote 3 recebido (1024 bytes)
[RDT] Pacote corrompido -> enviando NAK
[RDT] Pacote corrompido -> enviando NAK
[CANAL] NAK PERDIDO
[RDT] Pacote corrompido -> enviando NAK
[RDT] Pacote corrompido -> enviando NAK
[RDT] DADOS seq=0 OK -> enviando ACK 0
[CLIENTE] Pacote 4 recebido (1024 bytes)
[RDT] DADOS seq=1 OK -> enviando ACK 1
[CLIENTE] Pacote 5 recebido (1024 bytes)
[RDT] DADOS seq=0 OK -> enviando ACK 0
[CLIENTE] Pacote 6 recebido (1024 bytes)
[RDT] DADOS seq=1 OK -> enviando ACK 1
[CLIENTE] Pacote 7 recebido (1024 bytes)
[RDT] DADOS seq=0 OK -> enviando ACK 0
[CLIENTE] Pacote 8 recebido (1024 bytes)
[RDT] DADOS seq=1 OK -> enviando ACK 1
[CLIENTE] Pacote 9 recebido (1024 bytes)
[RDT] DADOS seq=0 OK -> enviando ACK 0
[CLIENTE] Pacote 10 recebido (1024 bytes)
[RDT] Pacote corrompido -> enviando NAK
[RDT] DADOS seq=1 OK -> enviando ACK 1
[CANAL] ACK 1 PERDIDO
[CLIENTE] Pacote 11 recebido (1024 bytes)
[RDT] Duplicata seq=1 (esperava 0) -> reenviando ACK 1
[CANAL] ACK 1 PERDIDO
[RDT] Duplicata seq=1 (esperava 0) -> reenviando ACK 1
[RDT] DADOS seq=0 OK -> enviando ACK 0
[CLIENTE] Pacote 12 recebido (471 bytes)
[RDT] DADOS seq=1 OK -> enviando ACK 1
[CANAL] ACK 1 PERDIDO
[CLIENTE] Arquivo salvo como 'arquivos_cliente\cliente_imagem1.jpg' (11735 bytes, 12 pacotes)
[CLIENTE] Aguardando em caso de retransmissão do FIM pelo servidor...
[RDT] Duplicata seq=1 após o fim -> reenviando ACK 1
[CANAL] ACK 1 PERDIDO
[RDT] Duplicata seq=1 após o fim -> reenviando ACK 1
[CANAL] ACK 1 PERDIDO
[RDT] Duplicata seq=1 após o fim -> reenviando ACK 1
[CLIENTE] Encerrado.
```

Exemplo de saída esperada no terminal servidor:

```
[RDT] DADOS seq=0 OK -> enviando ACK 0
[SERVIDOR] Início do arquivo 'imagem1.jpg' vindo de ('127.0.0.1', 49666)
[RDT] DADOS seq=1 OK -> enviando ACK 1
[SERVIDOR] Pacote 1 recebido (1024 bytes)
[RDT] DADOS seq=0 OK -> enviando ACK 0
[SERVIDOR] Pacote 2 recebido (1024 bytes)
[RDT] Pacote corrompido -> enviando NAK
[CANAL] NAK CORROMPIDO
[RDT] DADOS seq=1 OK -> enviando ACK 1
[SERVIDOR] Pacote 3 recebido (1024 bytes)
[RDT] DADOS seq=0 OK -> enviando ACK 0
[SERVIDOR] Pacote 4 recebido (1024 bytes)
[RDT] DADOS seq=1 OK -> enviando ACK 1
[SERVIDOR] Pacote 5 recebido (1024 bytes)
[RDT] DADOS seq=0 OK -> enviando ACK 0
[CANAL] ACK 0 PERDIDO
[SERVIDOR] Pacote 6 recebido (1024 bytes)
[RDT] Duplicata seq=0 (esperava 1) -> reenviando ACK 0
[RDT] DADOS seq=1 OK -> enviando ACK 1
[SERVIDOR] Pacote 7 recebido (1024 bytes)
[RDT] DADOS seq=0 OK -> enviando ACK 0
[SERVIDOR] Pacote 8 recebido (1024 bytes)
[RDT] DADOS seq=1 OK -> enviando ACK 1
[CANAL] ACK 1 PERDIDO
[SERVIDOR] Pacote 9 recebido (1024 bytes)
[RDT] Duplicata seq=1 (esperava 0) -> reenviando ACK 1
[RDT] DADOS seq=0 OK -> enviando ACK 0
[SERVIDOR] Pacote 10 recebido (1024 bytes)
[RDT] DADOS seq=1 OK -> enviando ACK 1
[SERVIDOR] Pacote 11 recebido (1024 bytes)
[RDT] DADOS seq=0 OK -> enviando ACK 0
[SERVIDOR] Pacote 12 recebido (471 bytes)
[RDT] DADOS seq=1 OK -> enviando ACK 1
[SERVIDOR] Arquivo salvo como 'arquivos_servidor\servidor_imagem1.jpg'(11735 bytes, 12 pacotes)
[SERVIDOR] Devolvendo imagem1.jpg para ('127.0.0.1', 49666)...
[RDT] Enviando DADOS seq=0 (18 bytes)
[CANAL] DADOS seq=0 PERDIDO
[RDT] TIMEOUT seq=0 -> retransmitindo
[RDT] Enviando DADOS seq=0 (18 bytes)[retransmissão 1]
[RDT] Resposta corrompida, ignorando
[RDT] TIMEOUT seq=0 -> retransmitindo
[RDT] Enviando DADOS seq=0 (18 bytes)[retransmissão 2]
[CANAL] DADOS seq=0 PERDIDO
[RDT] TIMEOUT seq=0 -> retransmitindo
[RDT] Enviando DADOS seq=0 (18 bytes)[retransmissão 3]
[RDT] ACK 0 recebido
[SERVIDOR] Pacote 1 devolvido (1024 bytes)
[RDT] Enviando DADOS seq=1 (1024 bytes)
[RDT] ACK 1 recebido
[SERVIDOR] Pacote 2 devolvido (1024 bytes)
[RDT] Enviando DADOS seq=0 (1024 bytes)
[RDT] ACK 0 recebido
[SERVIDOR] Pacote 3 devolvido (1024 bytes)
[RDT] Enviando DADOS seq=1 (1024 bytes)
[CANAL] DADOS seq=1 PERDIDO
[RDT] TIMEOUT seq=1 -> retransmitindo
[RDT] Enviando DADOS seq=1 (1024 bytes)[retransmissão 1]
[CANAL] DADOS seq=1 PERDIDO
[RDT] TIMEOUT seq=1 -> retransmitindo
[RDT] Enviando DADOS seq=1 (1024 bytes)[retransmissão 2]
[CANAL] DADOS seq=1 CORROMPIDO
[RDT] NAK recebido -> retransmitindo
[RDT] Enviando DADOS seq=1 (1024 bytes)[retransmissão 3]
[RDT] ACK 1 recebido
[SERVIDOR] Pacote 4 devolvido (1024 bytes)
[RDT] Enviando DADOS seq=0 (1024 bytes)
[CANAL] DADOS seq=0 CORROMPIDO
[RDT] NAK recebido -> retransmitindo
[RDT] Enviando DADOS seq=0 (1024 bytes)[retransmissão 1]
[CANAL] DADOS seq=0 CORROMPIDO
[RDT] TIMEOUT seq=0 -> retransmitindo
[RDT] Enviando DADOS seq=0 (1024 bytes)[retransmissão 2]
[CANAL] DADOS seq=0 PERDIDO
[RDT] TIMEOUT seq=0 -> retransmitindo
[RDT] Enviando DADOS seq=0 (1024 bytes)[retransmissão 3]
[CANAL] DADOS seq=0 CORROMPIDO
[RDT] NAK recebido -> retransmitindo
[RDT] Enviando DADOS seq=0 (1024 bytes)[retransmissão 4]
[CANAL] DADOS seq=0 CORROMPIDO
[RDT] NAK recebido -> retransmitindo
[RDT] Enviando DADOS seq=0 (1024 bytes)[retransmissão 5]
[RDT] ACK 0 recebido
[SERVIDOR] Pacote 5 devolvido (1024 bytes)
[RDT] Enviando DADOS seq=1 (1024 bytes)
[RDT] ACK 1 recebido
[SERVIDOR] Pacote 6 devolvido (1024 bytes)
[RDT] Enviando DADOS seq=0 (1024 bytes)
[CANAL] DADOS seq=0 PERDIDO
[RDT] TIMEOUT seq=0 -> retransmitindo
[RDT] Enviando DADOS seq=0 (1024 bytes)[retransmissão 1]
[CANAL] DADOS seq=0 PERDIDO
[RDT] TIMEOUT seq=0 -> retransmitindo
[RDT] Enviando DADOS seq=0 (1024 bytes)[retransmissão 2]
[RDT] ACK 0 recebido
[SERVIDOR] Pacote 7 devolvido (1024 bytes)
[RDT] Enviando DADOS seq=1 (1024 bytes)
[RDT] ACK 1 recebido
[SERVIDOR] Pacote 8 devolvido (1024 bytes)
[RDT] Enviando DADOS seq=0 (1024 bytes)
[CANAL] DADOS seq=0 PERDIDO
[RDT] TIMEOUT seq=0 -> retransmitindo
[RDT] Enviando DADOS seq=0 (1024 bytes)[retransmissão 1]
[RDT] ACK 0 recebido
[SERVIDOR] Pacote 9 devolvido (1024 bytes)
[RDT] Enviando DADOS seq=1 (1024 bytes)
[CANAL] DADOS seq=1 PERDIDO
[RDT] TIMEOUT seq=1 -> retransmitindo
[RDT] Enviando DADOS seq=1 (1024 bytes)[retransmissão 1]
[RDT] ACK 1 recebido
[SERVIDOR] Pacote 10 devolvido (1024 bytes)
[RDT] Enviando DADOS seq=0 (1024 bytes)
[RDT] ACK 0 recebido
[SERVIDOR] Pacote 11 devolvido (1024 bytes)
[RDT] Enviando DADOS seq=1 (1024 bytes)
[CANAL] DADOS seq=1 PERDIDO
[RDT] TIMEOUT seq=1 -> retransmitindo
[RDT] Enviando DADOS seq=1 (1024 bytes)[retransmissão 1]
[CANAL] DADOS seq=1 CORROMPIDO
[RDT] NAK recebido -> retransmitindo
[RDT] Enviando DADOS seq=1 (1024 bytes)[retransmissão 2]
[CANAL] DADOS seq=1 PERDIDO
[RDT] TIMEOUT seq=1 -> retransmitindo
[RDT] Enviando DADOS seq=1 (1024 bytes)[retransmissão 3]
[CANAL] DADOS seq=1 PERDIDO
[RDT] TIMEOUT seq=1 -> retransmitindo
[RDT] Enviando DADOS seq=1 (1024 bytes)[retransmissão 4]
[CANAL] DADOS seq=1 PERDIDO
[RDT] TIMEOUT seq=1 -> retransmitindo
[RDT] Enviando DADOS seq=1 (1024 bytes)[retransmissão 5]
[RDT] TIMEOUT seq=1 -> retransmitindo
[RDT] Enviando DADOS seq=1 (1024 bytes)[retransmissão 6]
[RDT] TIMEOUT seq=1 -> retransmitindo
[RDT] Enviando DADOS seq=1 (1024 bytes)[retransmissão 7]
[RDT] ACK 1 recebido
[SERVIDOR] Pacote 12 devolvido (471 bytes)
[RDT] Enviando DADOS seq=0 (471 bytes)
[CANAL] DADOS seq=0 PERDIDO
[RDT] TIMEOUT seq=0 -> retransmitindo
[RDT] Enviando DADOS seq=0 (471 bytes)[retransmissão 1]
[RDT] ACK 0 recebido
[RDT] Enviando DADOS seq=1 (3 bytes)
[RDT] TIMEOUT seq=1 -> retransmitindo
[RDT] Enviando DADOS seq=1 (3 bytes)[retransmissão 1]
[RDT] TIMEOUT seq=1 -> retransmitindo
[RDT] Enviando DADOS seq=1 (3 bytes)[retransmissão 2]
[CANAL] DADOS seq=1 PERDIDO
[RDT] TIMEOUT seq=1 -> retransmitindo
[RDT] Enviando DADOS seq=1 (3 bytes)[retransmissão 3]
[RDT] TIMEOUT seq=1 -> retransmitindo
[RDT] Enviando DADOS seq=1 (3 bytes)[retransmissão 4]
[CANAL] DADOS seq=1 CORROMPIDO
[RDT] TIMEOUT seq=1 -> retransmitindo
[RDT] Enviando DADOS seq=1 (3 bytes)[retransmissão 5]
[RDT] ACK 1 recebido
[SERVIDOR] Devolução concluída: 12 pacotes.
```

Ao rodar o programa, são criadas duas pastas: `arquivos_servidor`, pasta com arquivos recebidos e armazenados e a pasta `arquivos_cliente` , que armazena os arquivos recebidos. 

## Testes Realizados

Foram realizados teste com diferentes tamanhos, nos formatos .txt e .jpeg, com o objetivo de observar a diferença na quantidade de pacotes enviados. 

- Arquivo de teste `texto1.txt` (Texto de 10 linhas - 519 bytes)
- Arquivo de teste `texto2.txt` (Texto de 30 linhas - 2219 bytes)
- Arquivo de teste `texto3.txt` (Texto de 60 linhas - 5279 bytes)
- Arquivo de teste `imagem1.txt` (Imagem de 11.735 bytes)
- Arquivo de teste `imagem2.txt` (Imagem de 51.108 bytes)
- Arquivo de teste `imagem3.txt` (Imagem de 208.415 bytes)
