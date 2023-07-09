import socket, threading, os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '\\Functions and Variables')
from variables import *
from functions_server import *

try: 
    clients_connected = dict() # lista de clientes conectados (IP:PORTA)
    sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # conexão IPV4/TCP
    sock_tcp.bind((SERVER, PORT)) # atribuindo Porta e Local
    print(f'Servidor: {SERVER} / {PORT}')
    sock_tcp.listen() # deixando indefinido quantidade máxima de conexões
    while True:
        try:
            sock_client, info_client = sock_tcp.accept() # aceitando clientes (guardando PORTA:SOCKET respectivamente do cliente)
            print (f"O Cliente de IP: {info_client[0]}\nNa Porta: {info_client[1]} foi conectado!", info_client) # informando a conexão
            clients_connected[info_client[1]] = sock_client # adicionando o cliente ao dicionario de clientes conectados
            thread_client = threading.Thread(target=cliInteraction, args=(sock_client, info_client, clients_connected)) # adicionando uma thread para cada cliente
            thread_client.start() # iniciando a thread
        except:
            print(sys.exc_info())
            exit()
except:
    print ("Fail: ")
    exit()