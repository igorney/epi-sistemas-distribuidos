class Mensagem:
    def __init__(self, tipo, key=None, value=None, timestamp=None):
        self.tipo = tipo
        self.key = key
        self.value = value
        self.timestamp = timestamp

    def to_string(self):
        return f"{self.tipo},{self.key},{self.value},{self.timestamp}"

    @staticmethod
    def from_string(mensagem_str):
        tipo, key, value, timestamp = mensagem_str.split(",")
        return Mensagem(tipo, key, value, timestamp)
