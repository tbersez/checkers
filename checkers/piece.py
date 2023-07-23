import pygame
from .constants import SQUARE_SIZE, PIECES_RADIUS

class Piece:

    def __init__(self, color, row, col, owner = None) -> None:
        self.owner = owner
        self.color = color
        self.king: bool = False
        self.row: int = row
        self.col: int = col
        self.position: tuple = (None, None)
        
        self.computePosition()
    
    # GUI ---------------------------------------------------------------------
    def computePosition(self) -> None:
        self.position = (
            self.row * SQUARE_SIZE + SQUARE_SIZE // 2,
            self.col * SQUARE_SIZE + SQUARE_SIZE // 2
        )
    
    def drawPiece(self, win) -> None:
        """
        Draws piece to GUI.
        """
        pygame.draw.circle(win, self.color, self.position, PIECES_RADIUS)