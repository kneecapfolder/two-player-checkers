import socket
import random
import string

HOST = '127.0.0.1'
PORT = 12345

rooms = {}

def generate_room_code():
    random_code = ''.join(random.choice(string.ascii_letters) for _ in range(5))
    if random_code in rooms:
        return generate_room_code()
    return random_code


def connect_to_room(sock : socket.socket):
    action = sock.recv(4).decode()

    if action == 'make':
        print(f'creating new room..')
        sock.sendall(generate_room_code().encode())
    elif action == 'join':
        print('joining room..')

if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print('server is listening..')

    while True:
        sock, _ = server.accept()
        connect_to_room(sock)