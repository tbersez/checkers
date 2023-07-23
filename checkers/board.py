import pygame
from .constants import COLS, ROWS, PIECES_ROWS, BLACK, RED, BLUE, WHITE, SQUARE_SIZE, PIECES_RADIUS
from .piece import Piece

class Board:

    def __init__(self) -> None:
        self.board = [[None for _ in range(COLS)]for _ in range(ROWS)]

    # GUI ---------------------------------------------------------------------
    def drawBoard(self, win) -> None:
        """
        Draws checkers board.
        """
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, RED, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def drawPieces(self, win) -> None:
        """
        Draws pieces on the board.
        """
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] != None:
                    color = self.board[row][col].getColor()
                    pygame.draw.circle(win, color, (row * SQUARE_SIZE + SQUARE_SIZE // 2, col * SQUARE_SIZE + SQUARE_SIZE // 2), PIECES_RADIUS)

    # Board setup -------------------------------------------------------------
    def initialiseBoard(self) -> None:
        """
        Initialise the board with both players piece.
        Empty squares hold None.
        """
        for row in range(PIECES_ROWS):
            for col in range(row % 2, COLS, 2):
                self.board[row][col] = Piece(color=BLUE)
        for row in range(ROWS - PIECES_ROWS, ROWS):
            for col in range(row % 2, COLS, 2):
                self.board[row][col] = Piece(color=WHITE)
# TESTS
if __name__ == '__main__':
    board = Board()
    board.initialiseBoard()
    print(board.board)