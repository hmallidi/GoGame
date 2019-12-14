from .go_board import GoBoard


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

        self._turns = []

    def get_turn_name(self):
        if (self._curr_turn == GoBoard.BLACK):
            return "Black"
        return "White"

    def get_board_display(self):
        return str(self._go_board)

    def get_piece(self, x, y):
        try:
            return self._go_board[x, y]
        except ValueError:
            return None

    def get_score(self):
        return self._scores[GoBoard.BLACK], self._scores[GoBoard.WHITE]

    def add_to_score(self, score):
        self._scores[self._curr_turn] += score

    def move(self, x, y):
        if (x == 0 and y == 0):
            self.change_turn()
            return

        self.check_if_piece_is_at_location(x, y)

        self.save_curr_turn_info()
        self._go_board[x, y] = self._curr_turn

        no_pieces_captured = self.take_pieces(x, y)

        if no_pieces_captured:
            self.check_if_suicidal(x, y)

        self.check_if_ko()
        self.change_turn()

    def check_if_piece_is_at_location(self, x, y):
        if self._go_board.is_piece(self._go_board[x, y]):
            raise ValueError('Piece is already at those coordinates!')

    def check_if_suicidal(self, x, y):
        if self.get_num_liberties(x, y) == 0:
            self.go_to_prev_turn()
            raise ValueError('Suicidal Move! There are no liberties there!')

    def check_if_ko(self):
        try:
            if self._go_board == self._turns[-2].get_board():
                self.go_to_prev_turn()
                raise ValueError('Cannot make a redundant move!')
        except IndexError:
            pass

    def take_pieces(self, x, y):
        no_pieces_captured = True

        opponent_piece_color = None
        if (self._curr_turn == GoBoard.BLACK):
            opponent_piece_color = GoBoard.WHITE
        else:
            opponent_piece_color = GoBoard.BLACK

        for piece, (x1, y1) in self.get_surrounding_locations(x, y):
            if piece is opponent_piece_color and self.get_num_liberties(x1, y1) == 0:
                num_captured = len(self.get_group(x1, y1))
                if num_captured > 0:
                    no_pieces_captured = False

                self.capture_group(x1, y1)
                self.add_to_score(num_captured)

        return no_pieces_captured

    def change_turn(self):
        if (self._curr_turn == GoBoard.BLACK):
            self._curr_turn = GoBoard.WHITE
        else:
            self._curr_turn = GoBoard.BLACK

    def get_curr_turn_info(self):
        return self.TurnInfo(self._go_board.clone_board(), self._curr_turn,
                             self._scores.copy())

    def load_turn_info(self, turn_info):
        self._go_board, self._curr_turn, self._scores = turn_info.get_info()

    def save_curr_turn_info(self):
        self._turns.append(self.get_curr_turn_info())

    def go_to_prev_turn(self):
        self.load_turn_info(self._turns.pop())

    def get_surrounding_locations(self, x, y):
        liberties = (
            (x - 1, y), (x + 1, y),
            (x, y - 1), (x, y + 1),
        )

        surrounding = [
            (self.get_piece(x1, y1), (x1, y1)) for x1, y1 in liberties
            if self.get_piece(x1, y1) is not None
        ]

        return surrounding

    def get_group_liberties_helper(self, x, y, traversed):
        piece = self._go_board[x, y]

        if not self._go_board.is_piece(piece):
            return set([(x, y)])
        else:
            surrounding_locations = [
                (p, (x1, y1)) for p, (x1, y1)
                in self.get_surrounding_locations(x, y)
                if (p is piece or not self._go_board.is_piece(p)) and (x1, y1)
                not in traversed
            ]

            traversed.add((x, y))

            if len(surrounding_locations) == 0:
                return set()

            more_locations = [
                self.get_group_liberties_helper(x1, y1, traversed)
                for p, (x1, y1) in surrounding_locations
            ]

            return set.union(*more_locations)

    def get_group_helper(self, x, y, traversed):
        piece = self._go_board[x, y]

        surrounding_locations = [
            (p, (x1, y1))
            for p, (x1, y1) in self.get_surrounding_locations(x, y)
            if p is piece and (x1, y1) not in traversed
        ]

        traversed.add((x, y))

        if len(surrounding_locations) == 0:
            return traversed

        more_locations = [
            self.get_group_helper(x1, y1, traversed)
            for p, (x1, y1) in surrounding_locations
        ]

        return traversed.union(*more_locations)

    def capture_group(self, x, y):
        if not self._go_board.is_piece(self._go_board[x, y]):
            raise ValueError('Attempted to kill an empty group!')

        for x1, y1 in self.get_group(x, y):
            self._go_board.remove_piece(x1, y1)

    def get_group_liberties(self, x, y):
        return self.get_group_liberties_helper(x, y, set())

    def get_group(self, x, y):
        if not self._go_board.is_piece(self._go_board[x, y]):
            raise ValueError('Attempted to get an empty group!')

        return self.get_group_helper(x, y, set())

    def get_num_liberties(self, x, y):
        return len(self.get_group_liberties(x, y))
