import socket
import os

# Endereço e porta do servidor
server_address = ('127.0.0.1', 1099)

# Função para enviar requisições ao servidor e receber as respostas
def send_request(address, request):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(address)
    client_socket.send(request.encode())
    response = client_socket.recv(1024).decode()
    client_socket.close()
    return response

# Função para lidar com requisições de DOWNLOAD
def handle_download_request(peer_address, file_name, destination_folder):

    pass

# Obtenha o endereço IP do peer automaticamente
host = socket.gethostbyname(socket.gethostname())

# Crie o socket do peer
peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
peer_socket.bind((host, 0))  # O sistema operacional irá atribuir uma porta disponível automaticamente
peer_port = peer_socket.getsockname()[1]  # Obtenha a porta atribuída pelo sistema
peer_socket.listen(1)
print("Peer iniciado e aguardando conexões...")
print("Endereço IP do peer:", host)
print("Porta do peer:", peer_port)

# Variáveis para armazenar o status de conexão do peer com o servidor e informações do peer
joined = False
peer_info = {}

# Loop principal do peer
while True:
    # Menu interativo
    print("\nMENU INTERATIVO")
    print("1. JOIN")
    print("2. SEARCH")
    print("3. DOWNLOAD")
    print("4. Sair")

    option = input("Escolha uma opção: ")

    if option == "1":
        if not joined:
            # Capturar informações do peer
            peer_info["IP"] = host
            peer_info["Porta"] = peer_port
            peer_info["Pasta"] = input("Digite o caminho completo da pasta onde se encontram os arquivos: ")

            # Verificar se a pasta existe
            if not os.path.isdir(peer_info["Pasta"]):
                print("Pasta inválida.")
                continue

            # Listar os arquivos na pasta
            files = os.listdir(peer_info["Pasta"])
            peer_info["Arquivos"] = files

            # Conectar-se ao servidor somente se ainda não tiver se juntado
            join_request = f"JOIN;{peer_info['IP']};{peer_info['Porta']};{''.join(peer_info['Pasta'])};{','.join(peer_info['Arquivos'])}"
            response = send_request(server_address, join_request)

            if response == "JOIN_OK":
                # Tratamento da resposta JOIN_OK
                print("Sou peer", peer_info["IP"] + ":" + str(peer_info["Porta"]), "com arquivos", " ".join(peer_info["Arquivos"]))
                joined = True
            else:
                print("Não foi possível se juntar ao servidor.")

    elif option == "2":
        # Enviar uma requisição de SEARCH ao servidor
        file_name = input("Digite o nome do arquivo: ")
        search_request = "SEARCH:" + file_name
        response = send_request(server_address, search_request)

        if response.startswith("peers com arquivo solicitado"):
            # Tratamento da resposta SEARCH
            peer_list_str = response.split(":")[1]
            peer_list = peer_list_str.split(",")
            print("Peers com arquivo solicitado:", " ".join(peer_list))

    elif option == "3":
        if joined:
            # Enviar uma requisição de DOWNLOAD a um peer escolhido
            peer_address = input("Digite o endereço IP do peer: ")
            file_name = input("Digite o nome do arquivo: ")

            download_request = "DOWNLOAD:" + file_name
            peer_address = (peer_address, peer_port)  # Usamos a porta do próprio peer
            response = handle_download_request(peer_address, file_name, peer_info["Pasta"])

            if response == "DOWNLOAD_OK":
                print("Download do arquivo", file_name, "concluído com sucesso.")
        else:
            print("Você precisa se juntar ao servidor primeiro.")

    elif option == "4":
        print("Saindo...")
        break

# Fecha o socket do peer
peer_socket.close()