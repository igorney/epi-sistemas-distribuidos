import socket


# Função para enviar uma requisição ao servidor
def send_request(server_address, request):
    # Crie um socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conecte-se ao servidor
    client_socket.connect(server_address)

    # Envie a requisição ao servidor
    client_socket.send(request.encode())

    # Receba a resposta do servidor
    response = client_socket.recv(1024).decode()

    # Feche a conexão
    client_socket.close()

    return response


# Função para tratar a requisição DOWNLOAD
def handle_download_request(peer_info, filename):
    # Envie uma requisição de DOWNLOAD ao peer
    # ...

    # Receba o arquivo do peer
    # ...

    # Armazene o arquivo na pasta específica do peer
    # ...

    response = "DOWNLOAD_OK"
    return response


# Configuração do peer
host = "127.0.0.1"  # Endereço IP do peer
port = 8000  # Porta do peer
server_address = ("127.0.0.1", 1099)  # Endereço IP e porta do servidor

# Crie um socket TCP
peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associe o socket ao endereço e porta do peer
peer_socket.bind((host, port))

# Espere por conexões
peer_socket.listen(1)
print("Peer aguardando conexões...")

# Loop principal do peer
while True:
    # Aceite uma nova conexão
    client_socket, client_address = peer_socket.accept()
    print("Conexão estabelecida com:", client_address)

    # Receba a requisição do peer
    request = client_socket.recv(1024).decode()

    # Trate a requisição de acordo com o tipo
    if request.startswith("JOIN_OK"):
        # Exemplo de tratamento da resposta JOIN_OK
        peer_info = "127.0.0.1:8776"  # Informações do peer
        files = ["aula1.mp4", "aula2.mp4"]  # Arquivos do peer
        print("Sou peer", peer_info, "com arquivos", " ".join(files))
    elif request.startswith("peers com arquivo solicitado"):
        # Exemplo de tratamento da resposta SEARCH
        peer_list = request.split(":")[1].split(",")  # Lista de peers com o arquivo solicitado
        print("Peers com arquivo solicitado:", " ".join(peer_list))
    elif request.startswith("Arquivo"):
        # Exemplo de tratamento da resposta de arquivo baixado
        filename = request.split()[1]  # Nome do arquivo baixado
        folder = "nome_da_pasta"  # Pasta onde o arquivo foi armazenado
        print("Arquivo", filename, "baixado com sucesso na pasta", folder)

    # Trate outras requisições do peer, como DOWNLOAD
    # ...

    # Envie uma resposta de volta ao peer
    response = "OK"
    client_socket.send(response.encode())

    # Feche a conexão
    client_socket.close()
