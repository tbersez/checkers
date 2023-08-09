import pygame
from pygame.surface import Surface
from .board import Board
from .piece import Piece
from .moves import MoveTree
from .constants import PLAYER_WHITE, PLAYER_RED, SQUARE_SIZE, GREY, BLUE

class Game():
    """
    Internal representation of the game. Holds the board,
    game state (turns, remaining pieces, etc.). Runs turns
    checks, compute moves, checks for stoppage ...
    """

    MOVE_GUIDE_RADIUS = SQUARE_SIZE // 2 * .20
    CAPTURE_GUIDE_RADIUS = SQUARE_SIZE // 2 * .40

    def __init__(self, win: Surface) -> None:
        self.board: Board = Board()
        self.redPiecesCount: int = 0
        self.whitePiecesCount: int = 0
        self.win: Surface = win
        self.turn = PLAYER_RED
        self.selectedPiece: Piece|None = None
        self.validMoves: dict = None

        self.__updatePieceCounts()

    def __drawMoveGuides(self, coords: tuple) -> None:
        """
        Draws pieces move guides.
        """
        row, col = coords
        position = (
            row * SQUARE_SIZE + SQUARE_SIZE // 2,
            col * SQUARE_SIZE + SQUARE_SIZE // 2
        )
        pygame.draw.circle(self.win, GREY, position, self.MOVE_GUIDE_RADIUS)
    
    def __drawCaptureGuides(self, coords: tuple) -> None:
        """
        Draw capture guides.
        """
        row, col = coords
        position = (
            row * SQUARE_SIZE + SQUARE_SIZE // 2,
            col * SQUARE_SIZE + SQUARE_SIZE // 2
        )
        pygame.draw.circle(self.win, BLUE, position, self.CAPTURE_GUIDE_RADIUS)

    def updateGui(self) -> None:
        """
        Updates the GUI.
        """
        self.board.renderBoard(self.win)
        if self.validMoves:
            for move in self.validMoves.keys():
                self.__drawMoveGuides(move)
                if self.validMoves[move]:
                    for piece in self.validMoves[move]:
                        coords = piece.getCoords()
                        self.__drawCaptureGuides(coords)

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
                    tree = MoveTree(self.selectedPiece, self.board)
                    self.validMoves = tree.validMoves()
                    print(self.validMoves)
                    return True
            else:
                self.validMoves = None
        return False
    
    def __isInValidMove(self, coords) -> bool:
        """
        Checks if piece-to-coords is a valid move.
        Return true if it is, false otherwise.
        """
        for move in self.validMoves.keys():
            if coords == move:
                return True
        return False
    
    def __capture(self, coords: tuple) -> None:
        """
        Deletes captured pieces.
        """
        for piece in self.validMoves[coords]:
            self.board.delete(piece.getCoords())

    def __move(self, coords: tuple) -> bool:
        """
        Moves the selected piece to coordinates.
        Returns true upon success, false otherwise.
        """
        if self.selectedPiece is not None and self.__isInValidMove(coords):
            self.__capture(coords)
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