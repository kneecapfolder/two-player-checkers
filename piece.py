from enum import Enum
from customtkinter import CTkCanvas
from vector import *

class Team(Enum):
    BLUE = 1
    RED = 2

class Piece(Vector):
    counter = 1

    def __init__(self, x : int, y : int, team : Team):
        super().__init__(x, y)
        self.team = team
        self.id = Piece.counter
        Piece.counter += 1


    def draw(self, canvas : CTkCanvas):
        canvas.create_aa_circle(
            self.x*50+25, self.y*50+25, 20,
            fill=('red' if self.team == Team.RED else 'blue')
        )


    def on_team(self, team : Team):
        return self.team == team


    def __repr__(self):
        return f'Piece(\n    x: {self.x},\n    y: {self.y},\n    team: {self.team}\n)'