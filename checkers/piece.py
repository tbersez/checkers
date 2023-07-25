import pygame
from .constants import SQUARE_SIZE, GREY, GREEN

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
        
        self.__computePosition()
    
    def __repr__(self) -> str:
        return str(self.color)

    def getCoords(self) -> tuple:
        return (self.row, self.col)
    
    # Events ------------------------------------------------------------------
    def updateSelectedStatus(self):
        """
        Updates selected status of the piece.
        """
        self.selected = not self.selected
    
    def move(self, newCoords):
        """
        Updates row and col, then recompute position.
        """
        self.row, self.col = newCoords[0], newCoords[1]
        self.__computePosition()
    
    # GUI ---------------------------------------------------------------------
    def __computePosition(self) -> None:
        self.position = (
            self.row * SQUARE_SIZE + SQUARE_SIZE // 2,
            self.col * SQUARE_SIZE + SQUARE_SIZE // 2
        )
    
    def drawPiece(self, win) -> None:
        """
        Draws piece to GUI.
        """
        pygame.draw.circle(win, GREY, self.position, self.PADDING_RADIUS)
        if self.selected:
            pygame.draw.circle(win, GREEN, self.position, self.PIECES_RADIUS)
        else:
            pygame.draw.circle(win, self.color, self.position, self.PIECES_RADIUS)
    
    
        