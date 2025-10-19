import socket
import struct
import customtkinter as tk
from piece import *

class Move:
    def __init__(self, p : Piece, x : int, y : int, taken=None):
        self.p = p
        self.x = x
        self.y = y
        self.taken = taken




class BoardWindow:
    def __init__(self, sock : socket.socket, pieces : list[Piece], team : Team):
        self.sock = sock
        self.pieces = pieces
        self.team = team
        self.selected = None
        self.possible_moves = []
        self.my_turn = team == Team.BLUE

        # Set theme
        tk.set_appearance_mode("Dark")
        tk.set_default_color_theme('themes/red.json')
        self.my_font = lambda size: tk.CTkFont(size=size, weight='bold', family='Ariel')

        # Configure app window
        self.root = tk.CTk()
        self.root.geometry('440x440')
        self.root.title('Checkers')
        self.root.resizable(False, False)

        # Canvas
        self.canvas = tk.CTkCanvas(self.root, width=400, height=400, bg='black')
        self.canvas.pack(padx=20, pady=20)
        self.canvas.bind('<Button-1>', self.on_canvas_click)


    # Run app
    def start(self):
        self.draw_board()
        self.draw_pieces()
        self.root.mainloop()


    # +===============================+ draw +===============================+
    def draw_board(self):
        self.canvas.delete('all')
        for y in range(8):
            for x in range(0, 7, 2):
                self.canvas.create_rectangle((x+y%2)*50, y*50, (x+y%2)*50+50, y*50+50, fill='white')

    
    def draw_pieces(self):
        if self.selected:
            self.canvas.create_aa_circle(
                self.selected.x*50+25,
                self.selected.y*50+25,
                23, fill='white'
            )

        for p in self.pieces:
            p.draw(self.canvas)

        for move in self.possible_moves:
            self.canvas.create_aa_circle(
                move.x*50+25,
                move.y*50+25,
                6, fill='gray23'
            )


    # +===============================+ get info +===============================+
    def get_possible_moves(self):
        self.possible_moves = []
        for offset in [(-1, -1), (1, -1)]:
            if not self.find_piece(self.selected.x+offset[0], self.selected.y+offset[1]):
                self.possible_moves.append(
                    Move(
                        self.selected,
                        self.selected.x+offset[0],
                        self.selected.y+offset[1]
                    )
                )


    def find_piece(self, x : int, y : int) -> Piece:
        for p in self.pieces:
            if p.x == x and p.y == y:
                return p
        return None


    # +===============================+ change with board +===============================+
    def select_piece(self, p : Piece):
        if not p:
            self.selected = None
            self.possible_moves = []
            return
        self.selected = p
        self.get_possible_moves()

    
    def move_piece(self, move : Move):
        self.select_piece(None)
        self.my_turn = not self.my_turn

        if not self.my_turn:
            if move.taken:
                data = struct.pack('6h', move.p.x, move.p.y, move.x, move.y, move.taken.x, move.taken.y)
            else:
                data = struct.pack('6h', move.p.x, move.p.y, move.x, move.y, -1, -1)
            self.sock.sendall(data)
        
        (move.p.x, move.p.y) = (move.x, move.y)
        if move.taken:
            self.pieces.remove(move.taken)


    def on_canvas_click(self, event):
        if not self.my_turn:
            return

        x = event.x // 50
        y = event.y // 50
        print(x, y)

        self.perform_action(x, y)
        # print(self.selected.__repr__())
        
        self.draw_board()
        self.draw_pieces()


    def perform_action(self, x, y):
        if self.selected:
            # Deselect
            if self.selected.x == x and self.selected.y == y:
                self.select_piece(None)
                return
            
            # Try to move
            for option in self.possible_moves:
                if (x, y) == (option.x, option.y):
                    self.move_piece(option)
                    return

        # Select new piece
        p = self.find_piece(x, y)
        if p and p.on_team(self.team):
            self.select_piece(p)
        else:
            self.select_piece(None)

    
if __name__ == '__main__':
    pieces = []
    for y in range(3):
        for x in range(1, 8, 2):
            pieces.append(Piece(x-y%2, y, Team.RED))
    
    for y in range(3):
        for x in range(0, 7, 2):
            pieces.append(Piece(x+y%2, y+5, Team.BLUE))

    app = BoardWindow(pieces, Team.BLUE)
