from enum import Enum
from customtkinter import CTkCanvas

class Team(Enum):
    TEAM1 = 1
    TEAM2 = 2

class Piece:
    def __init__(self, x : int, y : int, team : Team):
        self.x = x
        self.y = y
        self.team = team


    def draw(self, canvas : CTkCanvas):
        canvas.create_aa_circle(self.x*50+25, self.y*50+25, 20)