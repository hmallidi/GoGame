from collections import namedtuple
from copy import copy

from .array import GoBoard


class GoGame(object):
    TURNS = (GoBoard.BLACK, GoBoard.WHITE)

    State = namedtuple('State', ['board', 'turn', 'score'])

    def __init__(self, size):
        self._scores = {
            GoBoard.BLACK: 0,
            GoBoard.WHITE: 0,
        }

        self._curr_turn = GoBoard.BLACK
        self._go_board = GoBoard(size, size)
        self._history = []

    def get_turn_name(self):
        if (self._curr_turn == GoBoard.BLACK):
            return "Black"
        return "White"

    def get_board_display(self):
        return str(self._go_board)

    def get_score(self):
        return self._scores[GoBoard.BLACK], self._scores[GoBoard.WHITE]

    def move(self, x, y):
        if (x == 0 and y == 0):
            self._change_turn()
            return

        if self._go_board.is_piece(self._go_board[x, y]):
            raise ValueError('Piece is already at those coordinates!')

        self._push_history()
        self._go_board[x, y] = self._curr_turn

        num_pieces_captured = self._take_pieces(x, y)

        if num_pieces_captured == 0:
            self._check_if_suicidal(x, y)

        self._check_for_ko()
        self._change_turn()

    def _check_if_suicidal(self, x, y):
        if self.get_num_liberties(x, y) == 0:
            self._go_to_prev_turn()
            raise ValueError('Suicidal Move! There are no liberties there!')

    def _check_for_ko(self):
        try:
            if self._go_board == self._history[-2].board:
                self._go_to_prev_turn()
                raise ValueError('Cannot make a redundant move!')
        except IndexError:
            pass

    def _take_pieces(self, x, y):
        scores = []

        opponent_piece_color = None
        if (self._curr_turn == GoBoard.BLACK):
            opponent_piece_color = GoBoard.WHITE
        else:
            opponent_piece_color = GoBoard.BLACK

        for piece, (x1, y1) in self._get_surrounding(x, y):
            if piece is opponent_piece_color and self.get_num_liberties(x1, y1) == 0:
                score = self._kill_group(x1, y1)
                scores.append(score)
                self._add_to_score(score)
        return sum(scores)

    def _change_turn(self):
        if (self._curr_turn == GoBoard.BLACK):
            self._curr_turn = GoBoard.WHITE
        else:
            self._curr_turn = GoBoard.BLACK

    def get_state(self):
        return self.State(self._go_board.copy(), self._curr_turn, copy(self._scores))

    def _load_state(self, state):
        self._go_board, self._curr_turn, self._scores = state

    def _push_history(self):
        self._history.append(self.get_state())

    def _go_to_prev_turn(self):
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
            return self._go_board[x, y]
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
        loc = self._go_board[x, y]

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
        if self._go_board[x, y] not in self.TURNS:
            raise ValueError('Can only get group for black or white location')

        return self._get_group(x, y, set())

    def _kill_group(self, x, y):
        if self._go_board[x, y] not in self.TURNS:
            raise ValueError('Can only kill black or white group')

        group = self.get_group(x, y)
        score = len(group)

        for x1, y1 in group:
            self._go_board.remove_piece(x1, y1)

        return score

    def _get_liberties(self, x, y, traversed):
        loc = self._go_board[x, y]

        if not self._go_board.is_piece(loc):
            # Return coords of empty location (this counts as a liberty)
            return set([(x, y)])
        else:
            # Get surrounding locations which are empty or have the same color
            # and whose coordinates have not already been traversed
            locations = [
                (p, (a, b))
                for p, (a, b) in self._get_surrounding(x, y)
                if (p is loc or not self._go_board.is_piece(p)) and (a, b) not in traversed
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
