import socket
from datetime import datetime

# Definindo o IP e a porta para o servidor
SERVER_IP = 'localhost'  # Use 'localhost' para testes locais
SERVER_PORT = 50000

# Criando o socket UDP
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_server:
    udp_server.bind((SERVER_IP, SERVER_PORT))
    print(f"Servidor UDP está rodando em {SERVER_IP}:{SERVER_PORT}...")
    
    while True:
        # Receber dados do cliente
        data, addr = udp_server.recvfrom(1024)
        print(f"Requisição recebida de {addr}: {data}")

        # Decodificar tipo de requisição
        tipo_requisicao = data[0]  # O tipo da requisição é o primeiro byte
        identificador = data[1:3]  # Identificador de 2 bytes
        
        if tipo_requisicao == 0x00:
            # Responder com data e hora
            resposta = f"{datetime.now():%a %b %d %H:%M:%S %Y}\n".encode('utf-8')
        elif tipo_requisicao == 0x01:
            # Responder com mensagem motivacional
            resposta = "Seja forte!\0".encode('utf-8')
        elif tipo_requisicao == 0x02:
            # Responder com quantidade de respostas (exemplo: 42)
            resposta = struct.pack('!I', 42)
        else:
            # Resposta para requisição inválida
            resposta = b''

        # Enviar a resposta para o cliente
        udp_server.sendto(resposta, addr)
