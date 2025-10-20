import socket
import struct
import customtkinter as tk
from piece import *



class BoardWindow:
    def __init__(self, sock : socket.socket, pieces : list[Piece], team : Team):
        self.sock = sock
        self.pieces = pieces
        self.team = team
        self.selected = 0
        self.possible_moves : list[Vector] = []
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
        print('boom')
        if self.selected:
            self.canvas.create_aa_circle(
                self.selected.x*50+25,
                self.selected.y*50+25,
                23, fill='white'
            )

        for p in self.pieces:
            p.draw(self.canvas)

        for pos in self.possible_moves:
            self.canvas.create_aa_circle(
                pos.x*50+25,
                pos.y*50+25,
                6, fill='gray23'
            )


    # +===============================+ get info +===============================+
    def get_possible_moves(self):
        self.possible_moves = []
        for offset in [(-1, -1), (1, -1)]:
            curr_pos = self.selected + offset
            p = self.find_piece(curr_pos.x, curr_pos.y)
            if not p:
                self.possible_moves.append(self.selected + offset)
            elif not p.on_team(self.team) and not self.find_piece(p.x + offset[0], p.y + offset[1]):
                self.possible_moves.append(p + offset)


    def find_piece(self, x : int, y : int) -> Piece:
        for p in self.pieces:
            if p.compareVec(x, y):
                return p
        return None
    

    def get_by_id(self, id : int):
        for p in self.pieces:
            if p.id == id:
                return p
        return None


    # +===============================+ change with board +===============================+
    def select_piece(self, p : int):
        if not p:
            self.selected = None
            self.possible_moves = []
            return
        self.selected = p
        self.get_possible_moves()

    
    def move_piece(self, p : Piece, newPos : Vector):
        self.select_piece(None)
        self.my_turn = not self.my_turn

        if abs(newPos.x - p.x) == 2:
            self.pieces.remove(self.find_piece(
                (p.x + newPos.x) / 2,
                (p.y + newPos.y) / 2 
            ))

        p.setVec(newPos)

        if not self.my_turn:
            data = struct.pack('3h', p.id, newPos.x, newPos.y)
            self.sock.sendall(data)


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
                if option.compareVec(x, y):
                    self.move_piece(self.selected, option)
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
