import math

from .array import Array
from .board import Board


class View(Array):
    def __init__(self, board):
        self._board = board
        self._star_point_coords = self._get_star_point_coords(board._width)

        super(View, self).__init__(
            board._width,
            board._height,
        )

    def _reset(self):
        self._array = [
            [str(loc) for loc in row]
            for row in self._board._array
        ]

        for i in self._star_point_coords:
            if self[i] == str(Board.EMPTY):
                self[i] = self.STAR_POINT

    def redraw(self):
        self._reset()

    def __str__(self):
        return '\n\n'.join(['    '.join(row) for row in self._array])
