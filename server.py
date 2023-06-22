import socket

s = socket.socket()
print("Socket created with success")
port = 12345
s.bind(('', port))
print("socket binded to port:", port)
s.listen(5)
print("socket is listening...")

while True:
    c, addr = s.accept()
    print("get connection from:", addr)
    s.send('Thank you for connecting'.encode())
    c.close()
    break
