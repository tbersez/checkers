from .piece import Piece
from .board import Board
from .constants import ROWS, COLS, PLAYER_WHITE

class MoveNode:
    """
    Node class for move tree.
    """
    
    def __init__(self, coords: tuple, lastJumped: Piece|None) -> None:
        self.children: dict = dict()
        self.coords: tuple = coords
        self.lastJumped: Piece|None = lastJumped
    
    def __repr__(self) -> str:
        return "Move to: {}, captures: {}".format(self.coords, self.lastJumped)
    
    def getCoords(self) -> tuple:
        """
        Get method for coords.
        """
        return self.coords

    def getChildren(self) -> dict:
        """
        Get method for children.
        """
        return self.children

class MoveTree():
    """
    Main class for move tree computation.
    Hold moving rules and jumping algorithm.
    """

    def __init__(self, piece: Piece, board: Board):
        self.root = MoveNode(
            coords = piece.getCoords(),
            lastJumped = None
        )
        self.board = board
        self.piece = piece
        if self.piece.getOwner() == PLAYER_WHITE:
            self.direction = 1
        else:
            self.direction = -1

    def printTree(self, node: MoveNode) -> None:
        """
        PRINTS TREE TO CLI FOR DEBUG
        """
        print(node)
        for child in node.getChildren().values():
            self.printTree(child)

    # Tree --------------------------------------------------------------------
    def buildTree(self, node: MoveNode, hasCaptured = False):
        """
        Builds move tree for a given piece.
        """
        if not self.piece.king:
            captures = self.__manCapture(node.getCoords())
            if captures:
                for capture in captures:
                    move, target = capture
                    node.children[move] = MoveNode(move, lastJumped = target)
                    for child in node.getChildren().values():
                        self.buildTree(child, hasCaptured = True)
            elif hasCaptured == False:
                moves = self.__manMove(node.getCoords())
                for move in moves:
                    node.children[move] = MoveNode(move, lastJumped = None)
        else:
            pass
    
    def getValidMoves(self, node: MoveNode) -> list:
        """
        Returns a list of valid moves for a piece.
        """
        
    # Moving rules ------------------------------------------------------------
    def __withinBounds(self, coords) -> bool:
        """
        Checks if coordinates are within bounds.
        """
        row, col = coords
        if (row >= 0 and row < ROWS) and (col >= 0 and col < COLS):
            return True
        return False
    
    def __manMove(self, coords: tuple) -> list:
        """
        Returns a list of possible man moves.
        """
        row, col = coords
        moves = []
        rowUp = (row + self.direction, col + 1)
        if self.__withinBounds(rowUp):
            if self.board.getSquareContent(rowUp) is None:
                moves.append(rowUp)
        rowDown = (row + self.direction, col - 1)
        if self.__withinBounds(rowDown):
            if self.board.getSquareContent(rowDown) is None:
                moves.append(rowDown)
        return moves

    def __manCapture(self, coords: tuple) -> list:
        """
        Returns a list of possible man captures.
        """
        row, col = coords
        moves = []
        targetUp = (row + self.direction, col + 1)
        moveUp = (row + 2 * self.direction, col + 2)
        if self.__withinBounds(targetUp) and self.__withinBounds(moveUp):
            target = self.board.getSquareContent(targetUp)
            if self.board.getSquareContent(moveUp) is None:
                if target is not None:
                    if target.getOwner() != self.piece.getOwner():
                        moves.append((moveUp, target))
        targetDown = (row + self.direction, col - 1)
        moveDown = (row + 2 * self.direction, col - 2)
        if self.__withinBounds(targetDown) and self.__withinBounds(moveDown):
            target = self.board.getSquareContent(targetDown)
            if self.board.getSquareContent(moveDown) is None:
                if target is not None:
                    if target.getOwner() != self.piece.getOwner():
                        moves.append((moveDown, target))
        return moves