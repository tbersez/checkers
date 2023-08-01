import pygame
from .constants import COLS, ROWS, PIECES_ROWS, RED, GREEN, BEIGE, WHITE, SQUARE_SIZE
from .piece import Piece

class Board:

    def __init__(self) -> None:
        self.board = [[None for _ in range(COLS)]for _ in range(ROWS)]

        self.__initialiseBoard()

    # GUI ---------------------------------------------------------------------
    def __drawBoard(self, win) -> None:
        """
        Draws checkers board.
        """
        win.fill(WHITE)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, GREEN, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    def __drawPieces(self, win) -> None:
        """
        Draws pieces on the board.
        """
        for row in range(ROWS):
            for col in range(COLS):
                if type(self.board[row][col]) == Piece:
                    self.board[row][col].drawPiece(win)

    def renderBoard(self, win) -> None:
        """
        Draws board and pieces.
        """
        self.__drawBoard(win)
        self.__drawPieces(win)

    # Board setup -------------------------------------------------------------
    def __initialiseBoard(self) -> None:
        """
        Initialise the board with both players pieces.
        Empty squares hold None.
        """
        for col in range(PIECES_ROWS):
            for row in range((col + 1) % 2, COLS, 2):
                self.board[row][col] = Piece(color=BEIGE, row=row, col=col)
        for col in range(ROWS - PIECES_ROWS, ROWS):
            for row in range((col + 1) % 2, COLS, 2):
                self.board[row][col] = Piece(color=RED, row=row, col=col)