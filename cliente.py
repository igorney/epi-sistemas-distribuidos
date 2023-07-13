import socket

from mensagem import Mensagem


class Cliente:
    def __init__(self, ip_servidor, porta_servidor):
        self.ip_servidor = ip_servidor
        self.porta_servidor = porta_servidor

    def iniciar(self):
        self.exibir_menu()

    def exibir_menu(self):
        while True:
            print("Menu Interativo:")
            print("1. INIT")
            print("2. PUT")
            print("3. GET")
            print("4. Sair")

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.inicializar_cliente()
            elif opcao == "2":
                self.enviar_requisicao_put()
            elif opcao == "3":
                self.enviar_requisicao_get()
            elif opcao == "4":
                break
            else:
                print("Opção inválida. Tente novamente.")

    def inicializar_cliente(self):
        mensagem = Mensagem("INIT", self.ip_servidor, self.porta_servidor)
        self.enviar_mensagem(mensagem)

    def enviar_requisicao_put(self):
        key = input("Digite a chave: ")
        value = input("Digite o valor: ")

        # mensagem = Mensagem("PUT", self.ip_servidor,
        #                     self.porta_servidor, key=key, value=value)
        # self.enviar_mensagem(mensagem)

    def enviar_requisicao_get(self):
        key = input("Digite a chave: ")

        # mensagem = Mensagem("GET", self.ip_servidor,
        #                     self.porta_servidor, key=key)
        # self.enviar_mensagem(mensagem)

    def enviar_mensagem(self, mensagem):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.ip_servidor, self.porta_servidor))
        client_socket.send(mensagem.to_string().encode())

        response = client_socket.recv(1024).decode()
        print(response)

        client_socket.close()
