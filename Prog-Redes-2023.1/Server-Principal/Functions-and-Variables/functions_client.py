import socket, time
from variables import *
from functions_others import *

# ============================================================================================================


def UPLOAD_SEND(name_arquive, dir_atual, sock_tcp):
    try:
        dir_arquivo = dir_atual + f'\\{name_arquive}' # pegando o nome do arquivo fornecido e montando caminho absoluto
        if not os.path.exists(dir_arquivo): # verificando se o arquivo fornecido existe [tem que está na mesma pasta do client.py]
            print(f'\nO Arquivo que você pediu "{name_arquive}" não existe no seu diretorio atual!\n') # informando caso não exista
            return
        size_arq = os.path.getsize(dir_arquivo) # existindo ele pega o tamanho do arquivo
        msg_local = f'/u:{size_arq}:{name_arquive}' # e faço o envio do comando, nome e tamanho do arquivo 
        sock_tcp.send(msg_local.encode(UNICODE)) # enviando antecipadamente nome e tamanho
        with open(dir_arquivo, 'rb') as arquive: # lendo o arquivo 
            while True:
                dados_arq = arquive.read(BUFFER)
                if not dados_arq:
                    break
                sock_tcp.send(dados_arq) # enviando o arquivo
    except FileNotFoundError:
        print(f'\nO Arquivo que você pediu "{name_arquive}" não existe no seu diretorio atual!\n')
    except IndexError: # para caso não seja repassado todos os argumentos de /d
        print(f"\nInforme todos os argumentos/parametros necessários para essa opção\n")
    except:
        print(f'\nErro no momento de realizar o UPLOAD [lado cliente]{sys.exc_info()}')

# ============================================================================================================

def DOWNLOAD_RECV(sock_tcp, size, name, dir_atual):
    try:
        os.makedirs('Downloads', exist_ok=True)
        local_arquive = dir_atual + f'\\Downloads\\{name}'
        with open(local_arquive, 'wb') as arquivo:
            bytes_recebidos = 0
            pct = 1
            print(f'\nGravando o arquivo: {name}\nTamanho: {size} bytes')
            while True:
                # Recebendo o conteúdo do servidor
                data_arquive = sock_tcp.recv(BUFFER)
                if not data_arquive: break
                arquivo.write(data_arquive)
                bytes_recebidos += len(data_arquive)
                print(f'Pacote ({pct}) - Dados: {bytes_recebidos}/{size} bytes')
                if bytes_recebidos >= size: break
                pct += 1
        print('\nDownload Finalizado!\n')
    except FileNotFoundError:
        print(f'\nO Arquivo que você pediu "{name}" não existe no servidor!\nDê /f para consultar os arquivos existentes...\n')
        return
    except:
        print(f'Erro no recebimento do download Local...{sys.exc_info()}')

# ============================================================================================================

def CLOSE_SOCKET(sock_tcp):
    try:
        sock_tcp.close()
    except:
        None
    
# ============================================================================================================

def SERVER_INTERACTION(sock_tcp, dir_atual):
    try:
        while True:
            retorno = sock_tcp.recv(512)
            if not retorno:  # Verificar se o retorno é vazio, indicando que o socket foi fechado pelo cliente
                break
            msg = retorno.decode(UNICODE)
            if msg == '/q':
                print("\nConexão encerrada.\n")
                break
            if msg[:2] == '/d':
                info_arquive = COMAND_SPLIT(msg)
                size = int(info_arquive[1])
                name = info_arquive[2]
                DOWNLOAD_RECV(sock_tcp, size, name, dir_atual)
                continue
            print(msg)
    except:
        print(f'\nErro na interacao com o servidor... {sys.exc_info()}')
    finally:
        CLOSE_SOCKET(sock_tcp)

# ============================================================================================================

def USER_INTERACTION(sock_tcp, dir_atual):
    try:
        while True:
            msg = input(PROMPT)
            if msg[:2] == '/u':
                UPLOAD_SEND(msg[3:], dir_atual, sock_tcp)
                continue
            sock_tcp.send(msg.encode())
            if msg == '/q':
                print("\nConexão encerrada.\n")
                break
            time.sleep(0.5)
    except:
        print(f'\nErro na interacao com o Usuário... {sys.exc_info()}')
    finally:
        CLOSE_SOCKET(sock_tcp)

# ============================================================================================================
