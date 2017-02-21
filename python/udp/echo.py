import socket
import threading


def create_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        #s = socket.socket()
        host = 'localhost'
        port = 12345

        s.bind((host, port))

        data, addr = s.recvfrom(1024)
        print("received", addr, data.decode())


def create_client():
    while True:
        a = input()
        print("local", a)

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            host = 'localhost'
            port = 12345

            s.sendto(a.encode(), (host, port))

threading.Thread(target=create_server).start()
threading.Thread(target=create_client).start()
