import socket
import struct

HOST = '127.0.0.1'
PORT = 12345

class Client:
    def __init__(self, HOST : str, PORT : int, host : bool):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))

        # Room connection
        self.sock.sendall(b'make' if host else b'join')
        self.room_code, self.color = struct.unpack(self.sock.recv(9).decode())
        print(self.room_code)

if __name__ == '__main__':
    client = Client(HOST, PORT, True)