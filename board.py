from pieces import Piece, Pawn, Rook, Colors, Bishop
from exceptions import NonexistentSquareError

FILES = ["a", "b", "c", "d", "e", "f", "g", "h"]


class Square :
    """Object defined by a file/rank coordinate and the possession
    or absence of a piece."""

    def __init__(self, file, rank):

        self.file = file
        self.rank = rank
        self.piece = None

    def __str__(self):

        return self.file + self.rank

    def has_piece(self):

        return self.piece is not None


class Board :

    def __init__(self):
        self.squares = self.gen_board()
        self.white_pieces = []
        self.black_pieces = []
        self.diagonals = self.get_all_diagonals()
        self.set_pieces()

    def __str__(self):

        return str({str(i) : (str(i.piece), i.piece.color.value) for i in self.squares if i.piece != None})

    def gen_board(self):
        """Generates the board as a list of squares."""
        board = []

        for file in FILES:
            for i in range(1, 9):
                board.append(Square(file, str(i)))

        return board

    def get_square(self, coord):
        """Returns the square object of the board that corresponds to the string
        coordinate argument."""

        if len(coord) != 2:
            raise NonexistentSquareError(coord)

        try:
            return next(square for square in self.squares if square.file == coord[0] and square.rank == coord[1])
        except StopIteration:
            raise NonexistentSquareError(coord)

    def get_file(self, file):
        index = FILES.index(file)
        squares = []
        for i in range (0, 8):
            squares.append(self.squares[index * 8 + i])

        return squares

    def get_rank(self, rank):

        squares = []
        for i in range (0, 8):
            squares.append(self.squares[int(rank) - 1 + 8 * i])

        return squares

    def get_diagonal(self, origin, direction):
        """Given an origin square and a positive or negative direction,
        returns list of squares forming diagonal from origin towards direction.

        Direction should be 1 or - 1, representing positive or negative."""

        diagonal = [origin]
        cur_rank = int(origin.rank)
        cur_file = origin.file

        while True:
            try:
                cur_rank += 1
                next_file_index = FILES.index(cur_file) + direction
                if next_file_index < 0:
                    break
                cur_file = FILES[next_file_index]
                diagonal.append(self.get_square(cur_file + str(cur_rank)))
            except (NonexistentSquareError, IndexError):
                break

        return diagonal

    def get_all_diagonals(self):

        diags = {}

        a_file, h_file, first_rank = self.get_file("a"), self.get_file("h"), self.get_rank(1)
        a_file.pop()
        h_file.pop()
        first_rank.pop(0)

        for sq in a_file:
            diag = self.get_diagonal(sq, 1)
            diags.update({(diag[0], diag[-1]) : diag})

        for sq in first_rank:
            diag = self.get_diagonal(sq, 1)
            diags.update({(diag[0], diag[-1]) : diag})

            diag = self.get_diagonal(sq, -1)
            diags.update({(diag[0], diag[-1]): diag})

        for sq in h_file:
            diag = self.get_diagonal(sq, -1)
            diags.update({(diag[0], diag[-1]) : diag})

        return diags

    def set_pieces (self):

        for square in self.get_rank(2):
            square.piece = Pawn (Colors.WHITE, self)

        for square in self.get_rank(7):
            square.piece = Pawn(Colors.BLACK, self)


BOARD = Board()
DIAGONALS = BOARD.get_all_diagonals()


BOARD.get_square("c3").piece = Bishop(Colors.WHITE, BOARD)
moves = BOARD.get_square("c3").piece.legal_moves()

for m in moves:
    print(str(m))