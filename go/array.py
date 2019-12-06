from copy import copy


class Array(object):
    def __init__(self, width, height, empty=None):
        self._width = width
        self._height = height
        self._empty = empty

        self._reset()

    def _check_valid(self, x, y):
        if (x < 0 or x >= self._width or y < 0 or y >= self._height):
            raise ValueError('Coordinates ({}, {}) are out of bounds'.format(x + 1, y + 1))

    def __getitem__(self, coordinates):
        x, y = coordinates
        x, y = x - 1, y - 1

        self._check_valid(x, y)
        return self._array[y][x]

    def __setitem__(self, coordinates, value):
        x, y = coordinates
        x, y = x - 1, y - 1

        self._check_valid(x, y)
        self._array[y][x] = value

    def _reset(self, value=None):
        value = value or self._empty

        self._array = [
            [value for i in range(self._width)]
            for j in range(self._height)
        ]

    @property
    def copy(self):
        new = copy(self)
        new._array = [copy(row) for row in self._array]
        return new
