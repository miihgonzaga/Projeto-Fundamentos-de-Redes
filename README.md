# Projeto de Redes 2026.2 - Parte 1

**Universidade Federal de Pernambuco - UFPE**

**CIN 0018 - Fundamentos de Redes de Computadores**

**Docente:** Renato Mariz de Moraes

**Equipe 1 - Integrantes:** Miriam Gonzaga da Silva Santos, Maria Gabriella Medeiros da Silva, Lucas Jose Duarte Cavalcanti e Mario Daniel Teles da Silva Filho

# Transmissão de Arquivos com UDP

Esta parte do projeto implementa uma aplicação cliente-servidor através de transferência de arquivos via socket **UDP (User Datagram Protocol)** na linguagem Python, utilizando as bibliotecas socket, sys e os. 

Arquivos enviados do cliente são armazenados com o prefixo “servidor_” e devolvidos ao cliente com o prefixo “cliente_”. 

## Estrutura

- cliente.py (Arquivo python com o código do cliente UDP)
- servidor.py (Arquivo python com o código do servidor UDP)
- arquivos_teste  (Pasta de arquivos usados nos testes - formato txt e jpeg)
- arquivos_cliente (Pasta de arquivos devolvidos pelo servidor - prefixo “cliente_” e formato txt e jpeg)
- arquivos_servidor (Pasta de arquivos recebidos e salvos pelo servidor - prefixo “servidor_” e formato txt e jpeg)

## Como Executar

### Passo 1

Abrir dois terminais na pasta do projeto; 

### Passo 2

No primeiro terminal, inicie o servidor com o comando `python servidor.py`

Exemplo de saída esperada: `[SERVIDOR] escutando em 127.0.0.1:5000...`

### Passo 3

No segundo terminal, envie um arquivo do formato txt com o comando  `python cliente.py arquivos_teste/texto1.txt`  

Exemplo de saída esperada: 

```
[CLIENTE] Enviando arquivo 'texto1.txt'...
[CLIENTE] Pacote 1 enviado (519 bytes)
[CLIENTE] Envio concluído: 1 pacotes.
[CLIENTE] Aguardando devolução do servidor...
[CLIENTE] Recebendo devolução do arquivo 'texto1.txt'...
[CLIENTE] Pacote 1 recebido (519 bytes)
[CLIENTE] Arquivo salvo como 'arquivos_cliente\cliente_texto1.txt' (519 bytes, 1 pacotes)
```

Envie um arquivo do formato jpeg com o comando `python cliente.py arquivos_teste/imagem1.jpg`

Exemplo de saída esperada: 

```
[CLIENTE] Enviando arquivo 'imagem1.jpg'...
[CLIENTE] Pacote 1 enviado (1024 bytes)
[CLIENTE] Pacote 2 enviado (1024 bytes)
[CLIENTE] Pacote 3 enviado (1024 bytes)
[CLIENTE] Pacote 4 enviado (1024 bytes)
[CLIENTE] Pacote 5 enviado (1024 bytes)
[CLIENTE] Pacote 6 enviado (1024 bytes)
[CLIENTE] Pacote 7 enviado (1024 bytes)
[CLIENTE] Pacote 8 enviado (1024 bytes)
[CLIENTE] Pacote 9 enviado (1024 bytes)
[CLIENTE] Pacote 10 enviado (1024 bytes)
[CLIENTE] Pacote 11 enviado (1024 bytes)
[CLIENTE] Pacote 12 enviado (471 bytes)
[CLIENTE] Envio concluído: 12 pacotes.
[CLIENTE] Aguardando devolução do servidor...
[CLIENTE] Recebendo devolução do arquivo 'imagem1.jpg'...
[CLIENTE] Pacote 1 recebido (1024 bytes)
[CLIENTE] Pacote 2 recebido (1024 bytes)
[CLIENTE] Pacote 3 recebido (1024 bytes)
[CLIENTE] Pacote 4 recebido (1024 bytes)
[CLIENTE] Pacote 5 recebido (1024 bytes)
[CLIENTE] Pacote 6 recebido (1024 bytes)
[CLIENTE] Pacote 7 recebido (1024 bytes)
[CLIENTE] Pacote 8 recebido (1024 bytes)
[CLIENTE] Pacote 9 recebido (1024 bytes)
[CLIENTE] Pacote 10 recebido (1024 bytes)
[CLIENTE] Pacote 11 recebido (1024 bytes)
[CLIENTE] Pacote 12 recebido (471 bytes)
[CLIENTE] Arquivo salvo como 'arquivos_cliente\cliente_imagem1.jpg' (11735 bytes, 12 pacotes)
```

Ao rodar o programa, são criadas duas pastas: `arquivos_servidor`, pasta com arquivos recebidos e armazenados e a pasta `arquivos_cliente` , que armazena os arquivos recebidos. 

## Testes Realizados

Foram realizados teste com diferentes tamanhos, nos formatos .txt e .jpeg, com o objetivo de observar a diferença na quantidade de pacotes enviados. 

- Arquivo de teste `texto1.txt` (Texto de 10 linhas - 519 bytes)
- Arquivo de teste `texto2.txt` (Texto de 30 linhas)
- Arquivo de teste `texto3.txt` (Texto de 60 linhas)
- Arquivo de teste `imagem1.txt` (Imagem de 11.735 bytes)
- Arquivo de teste `imagem2.txt` (Imagem de 51.108 bytes)
- Arquivo de teste `imagem3.txt` (Imagem de 208.415 bytes)