"""Defines useful exceptions."""


class _SquareError (BaseException):
    """Base class for all exceptions related to the
    Square class"""

    pass


class NonexistentSquareError(_SquareError):

    def __init__(self, square):
        _SquareError.__init__(self)
        self.square = square

    def __str__(self):

        return """The square {} does not exist""".format(self.square)
