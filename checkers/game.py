import pygame
from pygame.surface import Surface
from pygame.font import Font
from .board import Board
from .piece import Piece
from .moves import MoveTree
from .constants import PLAYER_WHITE, PLAYER_RED, SQUARE_SIZE, GREY, BLUE, BLACK, WHITE, HEIGHT, WIDTH

class Game():
    """
    Internal representation of the game. Holds the board,
    game state (turns, remaining pieces, etc.). Runs turns
    checks, compute moves, checks for stoppage ...
    """

    MOVE_GUIDE_RADIUS = SQUARE_SIZE // 2 * .20
    CAPTURE_GUIDE_RADIUS = SQUARE_SIZE // 2 * .40
    END_GAME_MENU_HEIGHT = 400
    END_GAME_MENU_WIDTH = 250
    FONT = pygame.font.SysFont("tlwgtypo", 30)

    def __init__(self, win: Surface) -> None:
        self.board: Board = Board()
        self.redPiecesCount: int = 0
        self.whitePiecesCount: int = 0
        self.win: Surface = win
        self.turn = PLAYER_RED
        self.selectedPiece: Piece|None = None
        self.validMoves: dict = None
        self.endGame: bool = False

        self.__updatePieceCounts()

    # GUI ---------------------------------------------------------------------
    def __drawText(self, text: str, font: Font, color: tuple, coords: tuple) -> None:
        """
        Draws text to window.
        """
        textImg = font.render(text, True, color)
        self.win.blit(textImg, coords)
    
    def __drawEndGameMenu(self) -> None:
        """
        Draws endgame menu.
        """
        coords = (
            (HEIGHT - self.END_GAME_MENU_HEIGHT) // 2,
            (WIDTH - self.END_GAME_MENU_WIDTH) // 2,
            self.END_GAME_MENU_HEIGHT,
            self.END_GAME_MENU_WIDTH
        )
        # Draws menu box
        pygame.draw.rect(self.win, BLACK, tuple(x + 5 for x in coords)) # Menu shade
        pygame.draw.rect(self.win, GREY, coords)
        # Add message
        message = "The {} player won!".format("red" if self.turn == PLAYER_RED else "white")
        textImg = self.FONT.render(message, True, WHITE)
        coords = (
            (HEIGHT - textImg.get_width()) // 2,
            (WIDTH - textImg.get_height()) // 2 - (self.END_GAME_MENU_WIDTH // 3),
            self.END_GAME_MENU_HEIGHT,
            self.END_GAME_MENU_WIDTH
        )
        self.win.blit(textImg, coords)

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
        if self.endGame:
            self.__drawEndGameMenu()

    # EVENTS ------------------------------------------------------------------
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
        self.selectedPiece = None
        self.validMoves = None
        self.__updatePieceCounts()
        if self.redPiecesCount == 0 or self.whitePiecesCount == 0:
            self.__endGame()
        elif self.turn == PLAYER_RED:
            self.turn = PLAYER_WHITE
        else:
            self.turn = PLAYER_RED
    
    def __endGame(self) -> None:
        """
        Ends the game.
        """
        self.selectedPiece = None
        self.validMoves = None
        self.endGame = True