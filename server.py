import socket


# Função para tratar a requisição JOIN
def handle_join_request(peer_info):
    # Adicione o peer e suas informações à estrutura de dados do servidor
    # ...
    response = "JOIN_OK"
    return response


# Função para tratar a requisição SEARCH
def handle_search_request(filename):
    # Verifique quais peers possuem o arquivo solicitado
    # ...
    response = []  # Lista vazia ou com as informações dos peers
    return response


# Função para tratar a requisição UPDATE
def handle_update_request(peer_info, filename):
    # Atualize as informações do peer com o arquivo baixado
    # ...
    response = "UPDATE_OK"
    return response


# Configuração do servidor
host = "127.0.0.1"  # Endereço IP do servidor
port = 1099  # Porta do servidor

# Crie um socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associe o socket ao endereço e porta
server_socket.bind((host, port))

# Espere por conexões
server_socket.listen(1)
print("Servidor aguardando conexões...")

# Loop principal do servidor
while True:
    # Aceite uma nova conexão
    client_socket, client_address = server_socket.accept()
    print("Conexão estabelecida com:", client_address)

    # Receba a requisição do peer
    request = client_socket.recv(1024).decode()

    # Trate a requisição de acordo com o tipo
    if request.startswith("JOIN"):
        peer_info = request.split(":")[1]  # Extrai as informações do peer
        response = handle_join_request(peer_info)
    elif request.startswith("SEARCH"):
        filename = request.split(":")[1]  # Extrai o nome do arquivo
        response = handle_search_request(filename)
    elif request.startswith("UPDATE"):
        params = request.split(":")
        peer_info = params[1]  # Extrai as informações do peer
        filename = params[2]  # Extrai o nome do arquivo
        response = handle_update_request(peer_info, filename)

    # Envie a resposta de volta ao peer
    client_socket.send(response.encode())

    # Feche a conexão
    client_socket.close()
