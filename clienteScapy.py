from scapy.all import *
import random
import struct

# Definindo IP e porta do servidor
SERVER_IP = '15.228.191.109'
SERVER_PORT = 50000
CLIENT_PORT = random.randint(1024, 65535)

# Função para criar a mensagem UDP formatada
def criar_mensagem_udp(tipo_requisicao):
    identificador = random.randint(1, 65535)
    mensagem = struct.pack('!B', tipo_requisicao) + struct.pack('!H', identificador)
    return mensagem, identificador

# Função para calcular o checksum UDP
def calcular_checksum(pseudo_cabecalho, udp_header, udp_payload):
    soma = sum(struct.unpack('!HHHHHHHH', pseudo_cabecalho + udp_header)) + sum(struct.unpack('!B' * len(udp_payload), udp_payload))
    
    # Fazer wraparound (soma de carry bits)
    while soma >> 16:
        soma = (soma & 0xFFFF) + (soma >> 16)
    
    # Complemento de 1
    checksum = ~soma & 0xFFFF
    return checksum

# Função para enviar e receber pacotes com SCAPY
def enviar_requisicao_scapy(tipo_requisicao):
    # Criar a mensagem de aplicação
    mensagem, identificador = criar_mensagem_udp(tipo_requisicao)

    # Cabeçalho UDP
    udp_len = 8 + len(mensagem)  # 8 bytes de cabeçalho + tamanho do payload
    udp_header = struct.pack('!HHHH', CLIENT_PORT, SERVER_PORT, udp_len, 0)

    # Cabeçalho IP falso (pseudo cabeçalho IP)
    pseudo_cabecalho = struct.pack('!4s4sBBH', 
                                   socket.inet_aton('192.168.1.105'),  # IP de origem (mude para o IP do seu cliente)
                                   socket.inet_aton(SERVER_IP),        # IP de destino
                                   0, 17, udp_len)  # 0, Protocolo UDP (17), comprimento UDP

    # Calcular o checksum UDP
    checksum = calcular_checksum(pseudo_cabecalho, udp_header, mensagem)

    # Atualizar o checksum no cabeçalho UDP
    udp_header = struct.pack('!HHHH', CLIENT_PORT, SERVER_PORT, udp_len, checksum)

    # Construir o pacote IP + UDP usando SCAPY
    pacote_udp = IP(src='192.168.1.105', dst=SERVER_IP) / UDP(sport=CLIENT_PORT, dport=SERVER_PORT) / Raw(load=mensagem)

    # Enviar o pacote UDP
    resposta = sr1(pacote_udp, timeout=2)  # sr1 envia o pacote e recebe 1 resposta

    if resposta:
        # Interpretando a resposta recebida
        resposta_payload = resposta[Raw].load
        req_res, identificador_resposta, tamanho = struct.unpack('!BHH', resposta_payload[:5])
        resposta_str = resposta_payload[5:].decode('utf-8')
        return identificador_resposta, resposta_str
    else:
        return None, "Sem resposta do servidor."

# Função principal do cliente
def cliente_scapy():
    while True:
        print("\nEscolha uma opção:")
        print("1 - Data e hora atual")
        print("2 - Mensagem motivacional")
        print("3 - Quantidade de respostas emitidas pelo servidor")
        print("4 - Sair")
        escolha = input("Digite o número da opção: ")

        if escolha == '1':
            identificador, resposta = enviar_requisicao_scapy(0x00)
            print(f"Identificador: {identificador}, Resposta: {resposta}")
        elif escolha == '2':
            identificador, resposta = enviar_requisicao_scapy(0x01)
            print(f"Identificador: {identificador}, Resposta: {resposta}")
        elif escolha == '3':
            identificador, resposta = enviar_requisicao_scapy(0x02)
            print(f"Identificador: {identificador}, Resposta: {resposta}")
        elif escolha == '4':
            print("Encerrando cliente...")
            break
        else:
            print("Opção inválida! Escolha novamente.")

# Iniciando o cliente UDP com SCAPY
if __name__ == '__main__':
    cliente_scapy()
