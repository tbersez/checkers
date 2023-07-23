import pygame

class Piece:

    def __init__(self, color, owner = None) -> None:
        self.owner = owner
        self.color = color

    def getColor(self):
        return self.color