import pygame
from .constants import SQUARE_SIZE, GREY, CROWN, COLS

class Piece:

    PIECES_RADIUS = SQUARE_SIZE // 2 * .68
    PADDING_RADIUS = SQUARE_SIZE // 2 * .75

    def __init__(self, color, player, row, col) -> None:
        self.color = color
        self.player = player
        self.king: bool = False
        self.row: int = row
        self.col: int = col
        self.position: tuple = (None, None)
        self.selected = False
        
        self.__computePosition()
    
    def __repr__(self) -> str:
        return str(self.color)
    
    def __makeKing(self) -> None:
        """
        Makes man king.
        """
        self.king = True

    def getCoords(self) -> tuple:
        """
        Returns coordinates as tuple.
        """
        return (self.row, self.col)
    
    def getOwner(self):
        """
        Return the piece owner.
        """
        return self.player

    def move(self, coords: tuple):
        """
        Updates piece coordinates, then compute new position.
        """
        row, col = coords
        self.row = row
        self.col = col
        self.__computePosition()
        if (col == COLS) or (col == 0):
            self.__makeKing()
    
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
        pygame.draw.circle(win, self.color, self.position, self.PIECES_RADIUS)
        if self.king:
            x, y = self.position
            win.blit(CROWN,
                (x - CROWN.get_width()//2, y - CROWN.get_height()//2)
            )

        