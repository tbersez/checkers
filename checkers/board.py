import pygame
from .constants import COLS, ROWS, PIECES_ROWS, BLACK, RED, BLUE, WHITE, SQUARE_SIZE
from .piece import Piece

class Board:

    def __init__(self) -> None:
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        
        self.__initialiseBoard()

    # GUI ---------------------------------------------------------------------
    def __drawBoard(self, win) -> None:
        """
        Draws checkers board.
        """
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, RED, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    def __drawPieces(self, win) -> None:
        """
        Draws pieces on the board.
        """
        for row in range(ROWS):
            for col in range(COLS):
                if type(self.board[row][col]) == Piece:
                    self.board[row][col].drawPiece(win)

    def renderBoard(self, win):
        """
        Draws board and pieces.
        """
        self.__drawBoard(win)
        self.__drawPieces(win)

    # Board setup -------------------------------------------------------------
    def __initialiseBoard(self) -> None:
        """
        Initialise the board with both players piece.
        Empty squares hold None.
        """
        # Player one
        for col in range(PIECES_ROWS):
            for row in range((col + 1) % 2, COLS, 2):
                self.board[row][col] = Piece(color=WHITE, row=row, col=col)
        # Player two
        for col in range(ROWS - PIECES_ROWS, ROWS):
            for row in range((col + 1) % 2, COLS, 2):
                self.board[row][col] = Piece(color=BLUE, row=row, col=col)
    
    # Events ------------------------------------------------------------------
    def locatePiece(self, coords: tuple) -> Piece|None:
        """
        Returns piece if piece found at coords, else None
        """
        row, col = coords
        return self.board[row][col]
    
    def move(self, piece: Piece, coords: tuple) -> None:
        """
        Move pieces by updating row and col values of a piece
        """
        row, col = coords
        self.board[row][col], self.board[piece.row][piece.col] = self.board[piece.row][piece.col], self.board[row][col] # Updates the board
        piece.move(coords) # Updates the piece
        print("Moved piece {} to {}.".format(piece, coords))