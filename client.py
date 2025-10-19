import socket
from checkers import *
import threading
import struct

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
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    pieces = []
    for y in range(3):
        for x in range(1, 8, 2):
            pieces.append(Piece(x-y%2, y, Team.BLUE))
    
    for y in range(3):
        for x in range(0, 7, 2):
            pieces.append(Piece(x+y%2, y+5, Team.RED))

    board = BoardWindow(sock, pieces, Team.RED)
    threading.Thread(target=listen_to_move, args=(sock, board), daemon=True).start()
    board.start()













# class Client:
#     def __init__(self, HOST : str, PORT : int, host : bool):
#         self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.sock.connect((HOST, PORT))

#         # Room connection
#         self.sock.sendall(b'make' if host else b'join')
#         self.room_code, self.color = struct.unpack(self.sock.recv(9).decode())
#         print(self.room_code)

# if __name__ == '__main__':
#     client = Client(HOST, PORT, True)