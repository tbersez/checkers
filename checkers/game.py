import pygame
from .board import Board
from .constants import PLAYER_WHITE, PLAYER_RED

class Game():
    """
    Internal representation of the game. Holds the board,
    game state (turns, remaining pieces, etc.). Runs turns
    checks, compute moves, checks for stoppage ...
    """

    def __init__(self, win) -> None:
        self.board: Board = Board()
        self.turn = PLAYER_RED
        self.redPiecesCount: int = 0
        self.whitePiecesCount: int = 0
        self.win = win

        self.__updatePieceCounts()
        
    def updateGui(self) -> None:
        """
        Updates the GUI.
        """
        self.board.renderBoard(self.win)

    def __updatePieceCounts(self) -> None:
        """
        Updates piece counts for both players.
        """
        self.redPiecesCount = self.board.countPieces(PLAYER_RED)
        self.whitePiecesCount = self.board.countPieces(PLAYER_WHITE)