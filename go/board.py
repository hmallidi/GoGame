from collections import namedtuple
from copy import copy

from .array import Array


class Board(Array):
    BLACK = '○'
    WHITE = '●'
    EMPTY = '.'

    TURNS = (BLACK, WHITE)

    State = namedtuple('State', ['board', 'turn', 'score'])

    def __init__(self, size):
        super(Board, self).__init__(size, size, self.EMPTY)

        self._scores = {
            self.BLACK: 0,
            self.WHITE: 0,
        }

        self._curr_turn = self.BLACK

        self._history = []

    def get_turn_name(self):
        if (self._curr_turn == self.BLACK):
            return "Black"
        return "White"

    def get_score(self):
        return self._scores[self.BLACK], self._scores[self.WHITE]

    def move(self, x, y):
        if (x == 0 and y == 0):
            self._change_turn()
            return

        if self[x, y] is not self.EMPTY:
            raise ValueError('Piece is already at those coordinates!')

        self._push_history()
        self[x, y] = self._curr_turn

        num_pieces_captured = self._take_pieces(x, y)

        if num_pieces_captured == 0:
            self._check_if_suicidal(x, y)

        self._check_for_ko()
        self._change_turn()

    def _check_if_suicidal(self, x, y):
        if self.get_num_liberties(x, y) == 0:
            self._pop_history()
            raise ValueError('Suicidal Move! There are no liberties there!')

    def _check_for_ko(self):
        try:
            if self._array == self._history[-2][0]:
                self._pop_history()
                raise ValueError('Cannot make a redundant move!')
        except IndexError:
            # Insufficient history...let this one slide
            pass

    def _take_pieces(self, x, y):
        scores = []

        opponent_piece_color = None
        if (self._curr_turn == self.BLACK):
            opponent_piece_color = self.WHITE
        else:
            opponent_piece_color = self.BLACK

        for piece, (x1, y1) in self._get_surrounding(x, y):
            if piece is opponent_piece_color and self.get_num_liberties(x1, y1) == 0:
                score = self._kill_group(x1, y1)
                scores.append(score)
                self._add_to_score(score)
        return sum(scores)

    def _change_turn(self):
        if (self._curr_turn == self.BLACK):
            self._curr_turn = self.WHITE
        else:
            self._curr_turn = self.BLACK

    def get_state(self):
        return self.State(self.copy._array, self._curr_turn, copy(self._scores))

    def _load_state(self, state):
        self._array, self._curr_turn, self._scores = state

    def _push_history(self):
        self._history.append(self.get_state())

    def _pop_history(self):
        current_state = self.get_state()
        try:
            self._load_state(self._history.pop())
            return current_state
        except IndexError:
            return None

    def _add_to_score(self, score):
        self._scores[self._curr_turn] += score

    def _get_none(self, x, y):
        try:
            return self[x, y]
        except ValueError:
            return None

    def _get_surrounding(self, x, y):
        liberties = (
            (x, y - 1),
            (x + 1, y),
            (x, y + 1),
            (x - 1, y),
        )
        return filter(lambda i: bool(i[0]), [
            (self._get_none(a, b), (a, b))
            for a, b in liberties
        ])

    def _get_group(self, x, y, traversed):
        loc = self[x, y]

        # Get surrounding locations which have the same color and whose
        # coordinates have not already been traversed
        locations = [
            (p, (a, b))
            for p, (a, b) in self._get_surrounding(x, y)
            if p is loc and (a, b) not in traversed
        ]

        # Add current coordinates to traversed coordinates
        traversed.add((x, y))

        # Find coordinates of similar neighbors
        if locations:
            return traversed.union(*[
                self._get_group(a, b, traversed)
                for _, (a, b) in locations
            ])
        else:
            return traversed

    def get_group(self, x, y):
        if self[x, y] not in self.TURNS:
            raise ValueError('Can only get group for black or white location')

        return self._get_group(x, y, set())

    def _kill_group(self, x, y):
        if self[x, y] not in self.TURNS:
            raise ValueError('Can only kill black or white group')

        group = self.get_group(x, y)
        score = len(group)

        for x1, y1 in group:
            self[x1, y1] = self.EMPTY

        return score

    def _get_liberties(self, x, y, traversed):
        loc = self[x, y]

        if loc is self.EMPTY:
            # Return coords of empty location (this counts as a liberty)
            return set([(x, y)])
        else:
            # Get surrounding locations which are empty or have the same color
            # and whose coordinates have not already been traversed
            locations = [
                (p, (a, b))
                for p, (a, b) in self._get_surrounding(x, y)
                if (p is loc or p is self.EMPTY) and (a, b) not in traversed
            ]

            # Mark current coordinates as having been traversed
            traversed.add((x, y))

            # Collect unique coordinates of surrounding liberties
            if locations:
                return set.union(*[
                    self._get_liberties(a, b, traversed)
                    for _, (a, b) in locations
                ])
            else:
                return set()

    def get_liberties(self, x, y):
        return self._get_liberties(x, y, set())

    def get_num_liberties(self, x, y):
        return len(self.get_liberties(x, y))
