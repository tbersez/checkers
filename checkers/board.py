import pygame
from pygame.surface import Surface
from .constants import COLS, ROWS, PIECES_ROWS, RED, GREEN, BEIGE, WHITE, SQUARE_SIZE, PLAYER_RED, PLAYER_WHITE
from .piece import Piece

class Board:

    def __init__(self) -> None:
        self.board = [[None for _ in range(COLS)]for _ in range(ROWS)]

        self.__initialiseBoard()

    # GUI ---------------------------------------------------------------------
    def __drawBoard(self, win: Surface) -> None:
        """
        Draws checkers board.
        """
        win.fill(WHITE)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, GREEN, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    def __drawPieces(self, win: Surface) -> None:
        """
        Draws pieces on the board.
        """
        for row in range(ROWS):
            for col in range(COLS):
                if type(self.board[row][col]) == Piece:
                    self.board[row][col].drawPiece(win)

    def renderBoard(self, win: Surface) -> None:
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
        for row in range(PIECES_ROWS):
            for col in range((row + 1) % 2, COLS, 2):
                self.board[row][col] = Piece(color=BEIGE, player=PLAYER_WHITE, row=row, col=col)
        for row in range(COLS - PIECES_ROWS, ROWS):
            for col in range((row + 1) % 2, COLS, 2):
                self.board[row][col] = Piece(color=RED, player=PLAYER_RED, row=row, col=col)
                
    # Events ------------------------------------------------------------------
    def getSquareContent(self, coords) -> Piece|None:
        """
        Return square content
        """
        row, col = coords
        return self.board[row][col]
    
    def move(self, piece: Piece, coords):
        """
        Moves piece to coords.
        """
        pieceRow, pieceCol = piece.getCoords()
        rowTo, colTo = coords
        self.board[pieceRow][pieceCol], self.board[rowTo][colTo] = \
            self.board[rowTo][colTo], self.board[pieceRow][pieceCol]
        piece.move(coords)
    
    def delete(self, coords: tuple) -> None:
        """
        Deletes piece fron the board.
        """
        row, col = coords
        self.board[row][col] = None

    def countPieces(self, owner) -> int:
        """
        Returns the number of pieces, owned by the
        specified owner, left on the board.
        """
        count = 0
        for row in range(ROWS):
            for col in range(COLS):
                squareContent = self.getSquareContent((row, col))
                if type(squareContent) == Piece:
                    if squareContent.getOwner() == owner:
                        count += 1
        return count
