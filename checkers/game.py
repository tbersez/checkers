import pygame
from .piece import Piece
from .board import Board
from .constants import BLUE, WHITE, SQUARE_SIZE

class Game:

    MOVE_GUIDE_COLOR = (0, 255, 255)
    MOVE_GUIDE_RADIUS = SQUARE_SIZE // 2 * .3

    def __init__(self, win) -> None:
        self.board = Board()
        self.win = win
        self.turn = BLUE
        self.selectedPiece: Piece|None = None # In hand piece
        self.selectedSquare: tuple|None = None # "In hand" square
        self.validMoves: list = []

    # Instance values updates -------------------------------------------------
    def __emptyHand(self):
        """
        Drops selected piece and square
        """
        self.selectedPiece = None
        self.selectedSquare = None
        self.validMoves = []

    def __nextTurn(self):
        """
        Drops hand and moves to next turn.
        """
        self.__emptyHand()
        self.validMoves = []
        if self.turn == BLUE:
            self.turn = WHITE
        else:
            self.turn = BLUE

    # Compute moves -----------------------------------------------------------
    def __computeSinglePieceMoves(self, piece: Piece):
        """
        """
        self.validMoves = [] # Stores square coords where a move is possible for the piece
        moves = []
        pieceRow, pieceCol = piece.getCoords()
        direction = 1 if piece.color == WHITE else -1
        # Reckons base moves
        newCoords = (pieceRow + 1, pieceCol + direction)
        if self.board.squareIsWithinBounds(newCoords):
            if self.board.isEmptySquare(newCoords):
                moves.append(newCoords)
        newCoords = (pieceRow - 1, pieceCol + direction)
        if self.board.squareIsWithinBounds(newCoords):
            if self.board.isEmptySquare(newCoords):
                moves.append(newCoords)
        self.validMoves = moves

    # Events ------------------------------------------------------------------
    def selectPiece(self, coords: tuple) -> None:
        """
        Selects a piece on the board and trigers highlighting.
        """
        squareContent = self.board.locatePiece(coords)
        if self.selectedPiece is None: # If no piece in hand 
            if squareContent is not None: # If square[coords] has piece
                if squareContent.color == self.turn:
                    self.selectedPiece = squareContent
                    self.selectedPiece.updateSelectedStatus()
        elif self.selectedPiece is not None: # If piece in hand
            if squareContent is not None: # If square[coords] has piece
                if squareContent.color == self.turn:
                    self.selectedPiece.updateSelectedStatus() # De-select piece
                    self.selectedPiece = squareContent # Updates hand
                    self.selectedPiece.updateSelectedStatus() # Select piece

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

    def runTurn(self, coords: tuple):
        """
        """
        if self.selectedPiece is None: # If no piece in hand
            self.selectPiece(coords)
            print(self.selectedPiece)
            if self.selectedPiece is not None: # If selected a valid piece
                self.__computeSinglePieceMoves(self.selectedPiece)
        elif (self.selectedPiece is not None) and (not self.board.isEmptySquare(coords)):
            self.selectPiece(coords)
            self.__computeSinglePieceMoves(self.selectedPiece)
        elif self.selectedSquare is None and self.board.isEmptySquare(coords):
            self.selectSquare(coords)
            self.move()
            self.__nextTurn()

    # GUI ---------------------------------------------------------------------
    def __computeMoveGuidePosition(self, coords: tuple) -> tuple:
        """
        """
        row, col = coords
        return (row * SQUARE_SIZE + SQUARE_SIZE // 2, col * SQUARE_SIZE + SQUARE_SIZE // 2)
    
    def __drawMoveGuides(self) -> None:
        """
        Draw move guides to GUI based on valid moves for the selected piece.
        """
        for move in self.validMoves:
            guideCenter = self.__computeMoveGuidePosition(move)
            pygame.draw.circle(self.win, self.MOVE_GUIDE_COLOR, guideCenter, self.MOVE_GUIDE_RADIUS)

    def update(self):
        """
        Updates board display.
        """
        self.board.renderBoard(self.win)
        self.__drawMoveGuides()
        pygame.display.update()


        
    
    