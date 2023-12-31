from .piece import Piece
from .board import Board
from .constants import ROWS, COLS, PLAYER_WHITE

class MoveNode:
    """
    Node class for move tree. Node may have any number of children.
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
    
    def getLastJumped(self) -> bool:
        """
        Get method for last jumped piece.
        """
        return self.lastJumped

    def hasChildren(self) -> bool:
        """
        Returns true if node has children, false otherwise.
        """
        if self.children:
            return True
        return False

    def hasLastJumped(self) -> bool:
        """
        Returns true if node has last jumped, false otherwise.
        """
        if self.lastJumped:
            return True
        return False

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
        self.moves: dict = dict()

    def printTree(self, node: MoveNode) -> None:
        """
        PRINTS TREE TO CLI FOR DEBUG
        """
        print(node)
        for child in node.getChildren().values():
            self.printTree(child)

    # Tree --------------------------------------------------------------------
    def __buildTree(self, node: MoveNode, jumped: list, hasCaptured: bool = False):
        """
        Builds move tree for a given piece.
        """
        print("Jumped: {}".format(jumped))
        if not self.piece.king: # Man case
            captures = self.__manCapture(node.getCoords())
            if captures:
                for capture in captures:
                    move, target = capture
                    node.children[move] = MoveNode(move, lastJumped = target)
                    for child in node.getChildren().values():
                        self.__buildTree(child, hasCaptured = True, jumped = jumped)
            elif hasCaptured == False:
                moves = self.__manMove(node.getCoords())
                for move in moves:
                    node.children[move] = MoveNode(move, lastJumped = None)
        else: # King case
            captures = self.__kingCapture(node.getCoords(), jumped)
            if captures:
                print("Captures: {}".format(captures))
                for capture in captures:
                    move, target = capture
                    node.children[move] = MoveNode(move, lastJumped = target)
                    jumped.append(target.getCoords())
                    for child in node.getChildren().values():
                        self.__buildTree(child, hasCaptured = True, jumped = jumped)
            elif hasCaptured == False:
                moves = self.__kingMove(node.getCoords())
                for move in moves:
                    node.children[move] = MoveNode(move, lastJumped = None)


    def __getValidMoves(self, node: MoveNode, jumped: list) -> None:
        """
        Formats valid moves from the tree as a list of tuples
        (landing coordinates and captured pieces). The first move
        to the list correspond to the piece starting point.
        """
        skiped = jumped.copy()
        if node.hasLastJumped():
            skiped.append(node.getLastJumped())
            print(jumped)
        self.moves[node.coords] = skiped
        if node.hasChildren():
            for node in node.getChildren().values():
                self.__getValidMoves(node, skiped)
    
    def validMoves(self) -> dict:
        """
        Explore the move tree and returns a move dictionary.
        Format: coords -> captures
        """
        self.__buildTree(self.root, [])
        self.__getValidMoves(self.root, [])
        self.moves.pop(self.root.getCoords())
        return self.moves

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
        Returns a list of possible man captures as
        a list of tuples.
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
    
    def __kingMove(self, coords: tuple) -> list:
        """
        Returns a list of possible king moves.
        """
        moves = []
        directions = [ # Represents 4 diagonals
            (1, 1), (-1, -1),
            (1, -1), (-1, 1)
        ]
        for direction in directions:
            row, col =  coords # Set coordinates
            rowDir, colDir = direction # Set directions
            while (self.__withinBounds((row, col))):
                row += rowDir
                col += colDir
                moveCoords = (row, col)
                if self.__withinBounds(moveCoords):
                    if self.board.getSquareContent(moveCoords) is None:
                        moves.append(moveCoords)
                    else:
                        break
        return moves

    def __kingCapture(self, coords: tuple, jumped: list) -> list:
        """
        Returns a list of possible king captures as
        a list of tuples.
        """
        moves = []
        directions = [ # Represents 4 diagonals
            (1, 1), (-1, -1),
            (1, -1), (-1, 1)
        ]
        for direction in directions:
            row, col =  coords # Set coordinates
            rowDir, colDir = direction # Set directions
            while (self.__withinBounds((row, col))):
                row += rowDir
                col += colDir
                targetCoords = (row, col)
                landingCoords = (row + rowDir, col + colDir)
                if self.__withinBounds(targetCoords):
                    target = self.board.getSquareContent(targetCoords)
                    if target:
                        if target.getCoords() not in jumped:
                            if target.getOwner() != self.piece.getOwner():
                                if self.__withinBounds(landingCoords):
                                    if self.board.getSquareContent(landingCoords) is None:
                                        moves.append((landingCoords, target))
                                        break
                                    else:
                                        break
                            elif target.getOwner() == self.piece.getOwner():
                                break
        return moves