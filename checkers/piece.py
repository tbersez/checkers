import pygame
from .constants import SQUARE_SIZE, GREY

class Piece:

    PIECES_RADIUS = SQUARE_SIZE // 2 * .68
    PADDING_RADIUS = SQUARE_SIZE // 2 * .75

    def __init__(self, color, row, col) -> None:
        self.color = color
        self.king: bool = False
        self.row: int = row
        self.col: int = col
        self.position: tuple = (None, None)
        self.selected = False
        
        self.computePosition()
    
    def __repr__(self) -> str:
        return str(self.color)
    
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
        pygame.draw.circle(win, GREY, self.position, self.PADDING_RADIUS)
        pygame.draw.circle(win, self.color, self.position, self.PIECES_RADIUS)
        