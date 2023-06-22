import socket
import sys

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created with success")
    port = 80

    try:
        host_ip = socket.gethostbyname('www.google.com')
    except socket.gaierror:
        print("error: cannot resolve the hostname")
        sys.exit()

    s.connect((host_ip, port))

    print("Socket sucessfull conected with host ip:", host_ip)
except socket.error as error:
    print("Socket creation failed with error:", error)
