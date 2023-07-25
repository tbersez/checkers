import pygame
from .piece import Piece
from .board import Board
from .constants import RED, WHITE, SQUARE_SIZE

class Game:

    def __init__(self, win) -> None:
        self.board = Board()
        self.win = win
        self.turn = RED
        self.selectedPiece: Piece|None = None # In hand piece
        self.selectedSquare: tuple = None # "In hand" square

    def __emptyHand(self):
        """
        Drops selected piece and square
        """
        self.selectedPiece = None
        self.selectedSquare = None

    # Events ------------------------------------------------------------------
    def selectPiece(self, coords: tuple) -> None:
        """
        Selects a piece on the board and trigers highlighting.
        """
        if self.selectedPiece:
            # De-select in hand piece, if any
            self.selectedPiece.updateSelectedStatus()
        self.selectedPiece = self.board.locatePiece(coords)
        self.selectedPiece.updateSelectedStatus()

    def selectSquare(self, coords: tuple) -> None:
        """
        """
        self.selectedSquare = coords

    def move(self):
        """
        """
        if (self.selectedPiece is not  None) and (self.selectedSquare is not None):
            self.board.move(self.selectedPiece, self.selectedSquare)
            self.selectedPiece.updateSelectedStatus()
            self.__emptyHand()
    
    def runTurn(self, coords: tuple):
        """
        """
        print(coords)
        if self.selectedPiece is None:
            self.selectPiece(coords)
        elif self.selectedSquare is None:
            self.selectSquare(coords)
            self.move()
            self.__emptyHand()

    # GUI ---------------------------------------------------------------------
    def update(self):
        """
        Updates board display.
        """
        self.board.renderBoard(self.win)
        pygame.display.update()


        
    
    