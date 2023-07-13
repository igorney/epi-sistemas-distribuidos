import threading
import socket
import random

from mensagem import Mensagem


class Servidor:
    def __init__(self, ip, porta, ip_lider, porta_lider):
        self.ip = ip
        self.porta = porta
        self.ip_lider = ip_lider
        self.porta_lider = porta_lider
        self.tabela_hash = {}
        self.timestamp = 0
        self.lider = False

    def iniciar(self):
        self.registrar_no_lider()

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.ip, self.porta))
        server_socket.listen(5)

        print(f"Servidor {self.ip}:{self.porta} iniciado.")

        while True:
            cliente_socket, cliente_endereco = server_socket.accept()
            threading.Thread(target=self.atender_requisicao,
                             args=(cliente_socket,)).start()

    def atender_requisicao(self, cliente_socket):
        mensagem_str = cliente_socket.recv(1024).decode()
        mensagem = Mensagem.from_string(mensagem_str)

        if mensagem.tipo == "PUT":
            if self.lider:
                self.processar_put(mensagem)
            else:
                return # self.encaminhar_put(mensagem)
        elif mensagem.tipo == "REPLICATION":
            self.processar_replication(mensagem)
        elif mensagem.tipo == "REPLICATION_OK":
            self.processar_replication_ok(mensagem)
        elif mensagem.tipo == "GET":
            self.processar_get(mensagem)

        cliente_socket.close()

    def registrar_no_lider(self):
        mensagem = Mensagem("REGISTER", self.ip, self.porta)
        self.enviar_mensagem(self.ip_lider, self.porta_lider, mensagem)

    def enviar_mensagem(self, ip_destino, porta_destino, mensagem):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip_destino, porta_destino))
        client_socket.send(mensagem.to_string().encode())
        client_socket.close()

    def processar_put(self, mensagem):
        key = mensagem.key
        value = mensagem.value
        self.timestamp += 1

        if key in self.tabela_hash:
            self.tabela_hash[key] = (value, self.timestamp)
        else:
            self.tabela_hash[key] = (value, self.timestamp)

        self.replicar_put(mensagem)

        response = Mensagem("PUT_OK", key, value, self.timestamp)
        self.enviar_mensagem(mensagem.ip_origem,
                             mensagem.porta_origem, response)

    def replicar_put(self, mensagem):
        for ip, porta in self.obter_enderecos_outros_servidores():
            mensagem_replication = Mensagem(
                "REPLICATION", mensagem.key, mensagem.value, mensagem.timestamp)
            self.enviar_mensagem(ip, porta, mensagem_replication)

    def processar_replication(self, mensagem):
        key = mensagem.key
        value = mensagem.value
        timestamp = mensagem.timestamp

        self.tabela_hash[key] = (value, timestamp)

        response = Mensagem("REPLICATION_OK", key, value, timestamp)
        self.enviar_mensagem(self.ip_lider, self.porta_lider, response)

    def processar_replication_ok(self, mensagem):
        key = mensagem.key
        value = mensagem.value
        timestamp = mensagem.timestamp

        response = Mensagem("PUT_OK", key, value, timestamp)
        self.enviar_mensagem(mensagem.ip_origem,
                             mensagem.porta_origem, response)

    def processar_get(self, mensagem):
        key = mensagem.key
        timestamp_cliente = mensagem.timestamp

        if key in self.tabela_hash:
            value, timestamp_servidor = self.tabela_hash[key]
            response = Mensagem("GET", key, value, timestamp_servidor)
            response.timestamp_cliente = timestamp_cliente
        else:
            response = Mensagem("GET", key, "Key not found", None)
            response.timestamp_cliente = timestamp_cliente

        self.enviar_mensagem(mensagem.ip_origem,
                             mensagem.porta_origem, response)

    def obter_enderecos_outros_servidores(self):
        enderecos = [
            ("127.0.0.1", 10098),
            ("127.0.0.1", 10099)
        ]
        enderecos.remove((self.ip, self.porta))
        return enderecos


def main():
    ip_lider = "127.0.0.1"
    porta_lider = 10097

    servers = []

    for port in range(10097, 10100):
        server = Servidor("127.0.0.1", port, ip_lider, porta_lider)
        servers.append(server)

    random.shuffle(servers)
    servers[0].lider = True

    for server in servers:
        server.iniciar()


if __name__ == "__main__":
    main()
