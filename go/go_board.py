import copy


class GoBoard(object):
    BLACK = '○'
    WHITE = '●'
    EMPTY = '.'
    STAR_POINT = '+'

    def __init__(self, width, height):
        self._width = width
        self._height = height

        self._board = [
            [self.EMPTY for i in range(self._width)]
            for j in range(self._height)
        ]

        for coordinates in self.get_star_point_coords(self._width):
            self[coordinates] = self.STAR_POINT

    def get_width(self):
        return self._width

    def _check_valid(self, x, y):
        if (x < 0 or x >= self._width or y < 0 or y >= self._height):
            raise ValueError('Coordinates ({}, {}) are out of bounds'.format(x + 1, y + 1))

    def __getitem__(self, coordinates):
        x, y = coordinates
        x, y = x - 1, y - 1

        self._check_valid(x, y)
        return self._board[y][x]

    def __setitem__(self, coordinates, piece):
        x, y = coordinates
        x, y = x - 1, y - 1

        self._check_valid(x, y)
        self._board[y][x] = piece

    def remove_piece(self, x, y):
        if self.is_star_point(x, y):
            self[x, y] = self.STAR_POINT
        else:
            self[x, y] = self.EMPTY

    def is_star_point(self, x, y):
        return (x, y) in self.get_star_point_coords(self._width)

    def is_piece(self, piece):
        return piece is self.BLACK or piece is self.WHITE

    def get_star_point_coords(self, width):
        star_point_coordinates = tuple()

        if width == 9:
            star_point_coordinates = (
                (3, 3), (5, 3), (7, 3),
                (3, 5), (5, 5), (7, 5),
                (3, 7), (5, 7), (7, 7)
            )
        elif width == 13:
            star_point_coordinates = (
                (4, 4), (7, 4), (10, 4),
                (4, 7), (7, 7), (10, 7),
                (4, 10), (7, 10), (10, 10)
            )
        else:
            star_point_coordinates = (
                (4, 4), (10, 4), (16, 4),
                (4, 10), (10, 10), (16, 10),
                (4, 16), (10, 16), (16, 16)
            )
        return star_point_coordinates

    def clone_board(self):
        board_clone = copy.copy(self)
        board_clone._board = [row.copy() for row in self._board]
        
        return board_clone

    def __str__(self):
        return '\n\n'.join(['    '.join(row) for row in self._board])

    def __eq__(self, other_board):
        if self._width != other_board.get_width():
            return 0

        for x in range(1, self._width):
            for y in range(1, self._height):
                if self[x, y] != other_board[x, y]:
                    return 0

        return 1
