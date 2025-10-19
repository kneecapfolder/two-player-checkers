import socket
import threading
import struct
from checkers import *
# import random
# import string

HOST = '127.0.0.1'
PORT = 12345

def listen_to_move(sock : socket.socket, board : BoardWindow):
    while True:
        data = sock.recv(12)
        print('boom')
        px, py, x, y, taken_x, taken_y = struct.unpack('6h', data)
        if px != -1:
            move = Move(board.find_piece(7-px, 7-py), 7-x, 7-y, board.find_piece(7-taken_x, 7-taken_y))
        else:
            move = Move(board.find_piece(7-px, 7-py), 7-x, 7-y)
        board.move_piece(move)
        board.draw_board()
        board.draw_pieces()


if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)

    sock, _ = server.accept()

    pieces = []
    for y in range(3):
        for x in range(1, 8, 2):
            pieces.append(Piece(x-y%2, y, Team.RED))
    
    for y in range(3):
        for x in range(0, 7, 2):
            pieces.append(Piece(x+y%2, y+5, Team.BLUE))

    board = BoardWindow(sock, pieces, Team.BLUE)
    threading.Thread(target=listen_to_move, args=(sock, board), daemon=True).start()
    board.start()














# rooms = {}

# def generate_room_code():
#     random_code = ''.join(random.choice(string.ascii_letters) for _ in range(5))
#     if random_code in rooms:
#         return generate_room_code()
#     return random_code


# def connect_to_room(sock : socket.socket):
#     action = sock.recv(4).decode()

#     if action == 'make':
#         print(f'creating new room..')
#         sock.sendall(generate_room_code().encode())
#     elif action == 'join':
#         print('joining room..')

# if __name__ == '__main__':
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.bind((HOST, PORT))
#     server.listen()
#     print('server is listening..')

#     while True:
#         sock, _ = server.accept()
#         connect_to_room(sock)