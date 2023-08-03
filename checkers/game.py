import pygame
from pygame.surface import Surface
from .board import Board
from .piece import Piece
from .constants import PLAYER_WHITE, PLAYER_RED

class Game():
    """
    Internal representation of the game. Holds the board,
    game state (turns, remaining pieces, etc.). Runs turns
    checks, compute moves, checks for stoppage ...
    """

    def __init__(self, win: Surface) -> None:
        self.board: Board = Board()
        self.redPiecesCount: int = 0
        self.whitePiecesCount: int = 0
        self.win: Surface = win
        self.turn = PLAYER_RED
        self.selectedPiece: Piece|None = None
        self.validMoves: dict = {}

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
    
    def select(self, coords: tuple) -> bool:
        """
        Selects piece on the board from coordinates. If the
        coordinates hold no piece, or an opponent's piece,
        sets self.selectedPiece to None.
        Returns true upon success, false otherwise.
        """
        if self.selectedPiece:
            move = self.__move(coords)
            if not move:
                self.selectedPiece.updateSelectedStatus()
                self.selectedPiece = None
                self.select(coords)
        else:
            if self.selectedPiece:
                self.selectedPiece.updateSelectedStatus()
            squareContent = self.board.getSquareContent(coords)
            if squareContent is not None:
                if squareContent.getOwner() == self.turn:
                    self.selectedPiece = squareContent
                    self.selectedPiece.updateSelectedStatus()
                     # TODO: COMPUTE VALID MOVES
                    return True
        return False

    def __move(self, coords: tuple) -> bool:
        """
        Moves the selected piece to coordinates.
        Returns true upon success, false otherwise.
        """
        squareContent = self.board.getSquareContent(coords)
        if self.selectedPiece is not None and squareContent is None: #and coords in self.validMoves:
            self.board.move(self.selectedPiece, coords)
            self.selectedPiece.updateSelectedStatus()
            self.__nextTurn()
            return True
        return False
    
    def __nextTurn(self) -> None:
        """
        Moves on to next turn.
        """
        self.__updatePieceCounts()
        if self.turn == PLAYER_RED:
            self.turn = PLAYER_WHITE
        else:
            self.turn = PLAYER_RED
        self.selectedPiece = None
        self.validMoves = None