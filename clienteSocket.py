import socket
import struct
import random

# Definindo IP e porta do servidor
SERVER_IP = '15.228.191.109'
SERVER_PORT = 50000

# Função para criar uma requisição formatada
def criar_requisicao(tipo_requisicao):
    identificador = random.randint(1, 65535)
    # Formato da mensagem: req/res (4 bits), tipo (4 bits), identificador (16 bits)
    # req/res sempre será 0 (requisição)
    mensagem = struct.pack('!B', tipo_requisicao) + struct.pack('!H', identificador)
    return mensagem, identificador

# Função para enviar requisição e receber resposta
def enviar_requisicao(tipo_requisicao):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        # Criando a mensagem de requisição
        mensagem, identificador = criar_requisicao(tipo_requisicao)
        udp_socket.sendto(mensagem, (SERVER_IP, SERVER_PORT))
        # Recebendo resposta do servidor
        resposta, _ = udp_socket.recvfrom(1024)  # Tamanho máximo do buffer 1024 bytes
        
        # Decodificando a resposta
        req_res, identificador_resposta, tamanho = struct.unpack('!BHH', resposta[:5])
        resposta_str = resposta[5:].decode('utf-8')
        
        return identificador_resposta, resposta_str

# Função principal do cliente
def cliente_udp():
    while True:
        print("\nEscolha uma opção:")
        print("1 - Data e hora atual")
        print("2 - Mensagem motivacional")
        print("3 - Quantidade de respostas emitidas pelo servidor")
        print("4 - Sair")
        escolha = input("Digite o número da opção: ")

        if escolha == '1':
            identificador, resposta = enviar_requisicao(0x00)
            print(f"Identificador: {identificador}, Resposta: {resposta}")
        elif escolha == '2':
            identificador, resposta = enviar_requisicao(0x01)
            print(f"Identificador: {identificador}, Resposta: {resposta}")
        elif escolha == '3':
            identificador, resposta = enviar_requisicao(0x02)
            print(f"Identificador: {identificador}, Resposta: {resposta}")
        elif escolha == '4':
            print("Encerrando cliente...")
            break
        else:
            print("Opção inválida! Escolha novamente.")

# Iniciando o cliente UDP
if __name__ == '__main__':
    cliente_udp()
