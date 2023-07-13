import socket


# Estrutura de dados para armazenar as informações dos peers e seus arquivos
peer_data = {}


# Função para tratar a requisição JOIN
def handle_join_request(peer_info, folder_path, files):
    # Adicione o peer e suas informações à estrutura de dados do servidor
    peer_data[peer_info] = {
        'folder_path': folder_path,
        'files': files
    }

    response = "JOIN_OK"
    return response


# Função para tratar a requisição SEARCH
def handle_search_request(filename):
    # Verifique quais peers possuem o arquivo solicitado
    peers_with_file = []
    for peer_info, peer_info_data in peer_data.items():
        files = peer_info_data['files']
        folder_path = peer_info_data['folder_path']
        if filename in files:
            peers_with_file.append(peer_info)

    response = peers_with_file
    return response


# Função para tratar a requisição UPDATE
def handle_update_request(peer_info, filename):
    # Atualize as informações do peer com o arquivo baixado
    peer_data[peer_info]['files'].append(filename)

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
        params = request.split(";")
        peer_info = params[1]  # Extrai as informações do peer
        folder_path = params[3]  # Extrai a pasta do peer
        files = params[4:]  # Extrai a lista de arquivos do peer
        response = handle_join_request(peer_info, folder_path, files)
    elif request.startswith("SEARCH"):
        filename = request.split(":")[1]  # Extrai o nome do arquivo
        response = handle_search_request(filename)
        print("Peer", client_address[0], "solicitou arquivo", filename)
    elif request.startswith("UPDATE"):
        params = request.split(":")
        peer_info = params[1]  # Extrai as informações do peer
        filename = params[2]  # Extrai o nome do arquivo
        response = handle_update_request(peer_info, filename)

    # Envie a resposta de volta ao peer
    client_socket.send(str(response).encode())

    # Feche a conexão
    client_socket.close()