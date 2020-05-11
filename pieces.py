"""Script containing all piece-related code."""

from misc import if_assign
from enum import Enum

FILES = ["a", "b", "c", "d", "e", "f", "g", "h"]


class Colors (Enum):

    WHITE = "White"
    BLACK = "Black"


class Piece :

    def __init__(self, color, board):
        self.color = color
        self.board = board

    def get_pos(self):
        return next (square for square in self.board.squares if square.piece is self)

    def legal_moves(self, board):
        # Returns list of squares to which the piece can move on a given board.
        pass

    def get_opposite_color(self):

        opposite = if_assign(self.color is Colors.WHITE, Colors.BLACK, Colors.WHITE)
        return opposite


class Pawn (Piece):

    def __init__(self, color, board):
        Piece.__init__(self, color, board)
        self.has_moved = False

    def __str__(self):
        return "Pawn"

    def legal_moves(self):

        advancements = if_assign(self.has_moved, 1, 2) # Can the pawn advance two squares or just one?
        rank = int(self.get_pos().rank)
        next_rank = str(rank + 1)
        file_index = FILES.index(self.get_pos().file)

        # Find the squares in front of the pawn and check if they have any piece.
        # If they don't, add them to the legal moves of this pawn.

        legal_moves = self.board.get_file(self.get_pos().file)[rank:rank + advancements]
        legal_moves = list(filter(lambda x : x.piece is None, legal_moves))

        # Find the squares diagonally adjacent to the pawn. If they have an enemy piece,
        # add them to the legal moves.

        diagonal_coords = [FILES[file_index + 1] + next_rank, FILES[file_index - 1] + next_rank]
        capture_squares = [self.board.get_square(diagonal_coords[0]), self.board.get_square(diagonal_coords[1])]

        for sq in capture_squares:
            if sq.has_piece() and sq.piece.color is self.get_opposite_color():
                legal_moves.append(sq)

        return legal_moves


class Rook (Piece):


    def __str__(self):
        return "Rook"

    def legal_moves(self):

        pos = self.get_pos()
        legal_moves = []

        file = list(filter(lambda x : x.piece is not self, self.board.get_file(pos.file)))
        rank = list(filter(lambda x : x.piece is not self, self.board.get_rank(pos.rank)))

        for sq in file:
            if sq.piece is None:
                legal_moves.append(sq)
                continue
            if sq.piece.color is not self.color:
                legal_moves.append(sq)
                break
            # If none of previous cases, then friendly piece was found.
            break

        for sq in rank:
            if sq.piece is None:
                legal_moves.append(sq)
                continue
            if sq.piece.color is self.get_opposite_color():
                legal_moves.append(sq)
                break

        return legal_moves


class Bishop (Piece):

    def pos_in_list(self, pos, list):

        return pos in list


    def legal_moves(self):

        pos = self.get_pos()
        diags = self.board.diagonals.values()

        legal_diagonals = [diag for diag in diags if pos in diag]
        legal_moves = [item for sublist in legal_diagonals for item in sublist]
        legal_moves.remove(pos)

        return legal_moves




