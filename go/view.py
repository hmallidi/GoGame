import math

from .array import Array
from .board import Board


class View(Array):
    """
    Stores string array which is used to paint the board.
    """
    STAR_POINT = '+'

    def __init__(self, board):
        self._board = board
        self._star_points = self._get_star_points(board._width)

        super(View, self).__init__(
            board._width,
            board._height,
        )

    def _reset(self):
        # Draw pieces from board state
        self._array = [
            [str(loc) for loc in row]
            for row in self._board._array
        ]

        # Draw STAR_POINT points
        for i in self._star_points:
            if self[i] == str(Board.EMPTY):
                self[i] = self.STAR_POINT

    def redraw(self):
        self._reset()

    def _get_star_points(self, width):
        star_points = tuple()

        if width == 9:
            star_points = (
                (3, 3), (5, 3), (7, 3),
                (3, 5), (5, 5), (7, 5),
                (3, 7), (5, 7), (7, 7)
            )
        elif width == 13:
            star_points = (
                (4, 4), (7, 4), (10, 4),
                (4, 7), (7, 7), (10, 7),
                (4, 10), (7, 10), (10, 10)
            )
        else:
            star_points = (
                (4, 4), (10, 4), (16, 4),
                (4, 10), (10, 10), (16, 10),
                (4, 16), (10, 16), (16, 16)
            )
        return star_points

    def _in_width(self, v):
        return max(1, min(self._width, v))

    def _in_height(self, v):
        return max(1, min(self._height, v))

    def __str__(self):
        return '\n\n'.join(['    '.join(row) for row in self._array])
