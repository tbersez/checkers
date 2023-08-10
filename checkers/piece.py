import pygame
from .constants import SQUARE_SIZE, GREY, BLACK, CROWN, ROWS

class Piece:

    PIECES_RADIUS = SQUARE_SIZE // 2 * .68
    PADDING_RADIUS = SQUARE_SIZE // 2 * .75

    def __init__(self, color, player, row, col) -> None:
        self.color = color
        self.player = player
        self.king: bool = True
        self.row: int = row
        self.col: int = col
        self.position: tuple = (None, None)
        self.selected = False
        
        self.__computePosition()
    
    def __repr__(self) -> str:
        return "{0}".format(self.getCoords())
    
    def __makeKing(self) -> None:
        """
        Makes man king.
        """
        self.king = True
    
    def updateSelectedStatus(self) -> None:
        """
        Updates a peice selected status.
        The selected piece is highlighted in the GUI.
        """
        self.selected = not self.selected

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
        self.row, self.col = coords
        self.__computePosition()
        if (self.row == (ROWS - 1)) or (self.row == 0):
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
        if self.selected:
            pygame.draw.circle(win, BLACK, self.position, self.PADDING_RADIUS)
        else:
            pygame.draw.circle(win, GREY, self.position, self.PADDING_RADIUS)
        pygame.draw.circle(win, self.color, self.position, self.PIECES_RADIUS)
        if self.king:
            x, y = self.position
            win.blit(CROWN,
                (x - CROWN.get_width()//2, y - CROWN.get_height()//2)
            )

        