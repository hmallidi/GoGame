from collections import namedtuple
from copy import copy

from .array import GoBoard


class GoGame(object):
    TURNS = (GoBoard.BLACK, GoBoard.WHITE)

    class TurnInfo(object):
        def __init__(self, go_board, turn, scores):
            self._go_board = go_board
            self._turn = turn
            self._scores = scores

        def get_board(self):
            return self._go_board

        def get_info(self):
            return (self._go_board, self._turn, self._scores)

    def __init__(self, size):
        self._go_board = GoBoard(size, size)
        self._curr_turn = GoBoard.BLACK
        self._scores = {
            GoBoard.BLACK: 0,
            GoBoard.WHITE: 0,
        }

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
            self.change_turn()
            return

        if self._go_board.is_piece(self._go_board[x, y]):
            raise ValueError('Piece is already at those coordinates!')

        self.save_curr_turn_info()
        self._go_board[x, y] = self._curr_turn

        num_pieces_captured = self.take_pieces(x, y)

        if num_pieces_captured == 0:
            self.check_if_suicidal(x, y)

        self.check_if_ko()
        self.change_turn()

    def check_if_suicidal(self, x, y):
        if self.get_num_liberties(x, y) == 0:
            self.go_to_prev_turn()
            raise ValueError('Suicidal Move! There are no liberties there!')

    def check_if_ko(self):
        try:
            if self._go_board == self._history[-2].get_board():
                self.go_to_prev_turn()
                raise ValueError('Cannot make a redundant move!')
        except IndexError:
            pass

    def take_pieces(self, x, y):
        scores = []

        opponent_piece_color = None
        if (self._curr_turn == GoBoard.BLACK):
            opponent_piece_color = GoBoard.WHITE
        else:
            opponent_piece_color = GoBoard.BLACK

        for piece, (x1, y1) in self.get_surrounding(x, y):
            if piece is opponent_piece_color and self.get_num_liberties(x1, y1) == 0:
                score = self.kill_group(x1, y1)
                scores.append(score)
                self.add_to_score(score)
        return sum(scores)

    def change_turn(self):
        if (self._curr_turn == GoBoard.BLACK):
            self._curr_turn = GoBoard.WHITE
        else:
            self._curr_turn = GoBoard.BLACK

    def get_curr_turn_info(self):
        return self.TurnInfo(self._go_board.copy(), self._curr_turn,
                             copy(self._scores))

    def load_turn_info(self, turn_info):
        self._go_board, self._curr_turn, self._scores = turn_info.get_info()

    def save_curr_turn_info(self):
        self._history.append(self.get_curr_turn_info())

    def go_to_prev_turn(self):
        try:
            self.load_turn_info(self._history.pop())
        except IndexError:
            pass

    def add_to_score(self, score):
        self._scores[self._curr_turn] += score

    def get_none(self, x, y):
        try:
            return self._go_board[x, y]
        except ValueError:
            return None

    def get_surrounding(self, x, y):
        liberties = (
            (x - 1, y), (x + 1, y),
            (x, y - 1), (x, y + 1),
        )
        
        return filter(lambda i: bool(i[0]), [
            (self.get_none(a, b), (a, b))
            for a, b in liberties
        ])

    def get_group(self, x, y, traversed):
        piece = self._go_board[x, y]

        locations = [
            (p, (a, b))
            for p, (a, b) in self.get_surrounding(x, y)
            if p is piece and (a, b) not in traversed
        ]

        traversed.add((x, y))

        if locations:
            return traversed.union(*[
                self.get_group(a, b, traversed)
                for _, (a, b) in locations
            ])
        else:
            return traversed

    def get_group(self, x, y):
        if self._go_board[x, y] is not GoBoard.BLACK and self._go_board[x, y] is not GoBoard.WHITE:
            raise ValueError('Can only get group for black or white location')

        return self.get_group(x, y, set())

    def kill_group(self, x, y):
        if self._go_board[x, y] is not GoBoard.BLACK and self._go_board[x, y] is not GoBoard.WHITE:
            raise ValueError('Can only kill black or white group')

        group = self.get_group(x, y)
        score = len(group)

        for x1, y1 in group:
            self._go_board.remove_piece(x1, y1)

        return score

    def get_liberties(self, x, y, traversed):
        piece = self._go_board[x, y]

        if not self._go_board.is_piece(piece):
            return set([(x, y)])
        else:
            locations = [
                (p, (a, b)) for p, (a, b) in self.get_surrounding(x, y)
                if (p is piece or not self._go_board.is_piece(p)) and (a, b) not in traversed
            ]

            traversed.add((x, y))

            if locations is not None:
                return set.union(*[
                    self.get_liberties(a, b, traversed)
                    for p, (a, b) in locations
                ])
            else:
                return set()

    def get_liberties(self, x, y):
        return self.get_liberties(x, y, set())

    def get_num_liberties(self, x, y):
        return len(self.get_liberties(x, y))
