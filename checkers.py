import customtkinter as tk
from piece import *

class Move:
    def __init__():
        pass




class BoardWindow:
    def __init__(self, pieces : list[Piece], team : Team):
        self.pieces = pieces
        self.team = team
        self.selected = None
        self.possible_moves = []
        self.turn = team == Team.BLUE

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
                move[0]*50+25,
                move[1]*50+25,
                6, fill='gray23'
            )


    # +===============================+ get info +===============================+
    def get_possible_moves(self):
        self.possible_moves = []
        for offset in [(-1, -1), (1, -1)]:
            if not self.find_piece(offset[0], offset[1]):
                self.possible_moves.append(offset)


    def find_piece(self, x : int, y : int) -> Piece:
        for p in pieces:
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

    
    def move_piece(move):
        pass


    def on_canvas_click(self, event):
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
                if (x, y) == option:
                    (self.selected.x, self.selected.y) = option
                    self.select_piece(None)
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
