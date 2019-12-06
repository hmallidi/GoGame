from collections import namedtuple
from copy import copy

from .array import Array


class Board(Array):
    """
    Stores board locations.  Provides methods to carry out game logic.
    """

    BLACK = '○'
    WHITE = '●'
    EMPTY = '.'

    State = namedtuple('State', ['board', 'turn', 'score'])

    def __init__(self, size):
        super(Board, self).__init__(size, size, self.EMPTY)

        # Player scores
        self._scores = {
            self.BLACK: 0,
            self.WHITE: 0,
        }

        self._curr_turn = self.BLACK

        # Game history
        self._history = []

    @property
    def turn_name(self):
        """
        Gets the current turn.
        """
        if (self._curr_turn == self.BLACK):
            return "Black"
        return "White"

    @property
    def _next_turn(self):
        """
        Gets color of next turn.
        """
        if (self._curr_turn == self.BLACK):
            return self.WHITE
        return self.BLACK

    @property
    def score(self):
        """
        Gets the current score.
        """
        return self._scores[self.BLACK], self._scores[self.WHITE]

    def move(self, x, y):
        """
        Makes a move at the given location for the current turn's color.
        """
        if (x == 0 and y == 0):
            self._change_turn()
            return

        if self[x, y] is not self.EMPTY:
            raise ValueError('Piece is already at those coordinates!')

        # Store history and make move
        self._push_history()
        self[x, y] = self._curr_turn

        # Check if any pieces have been taken
        taken = self._take_pieces(x, y)

        # Check if move is suicidal.  A suicidal move is a move that takes no
        # pieces and is played on a coordinate which has no liberties.
        if taken == 0:
            self._check_if_suicidal(x, y)

        # Check if move is redundant.  A redundant move is one that would
        # return the board to the state at the time of a player's last move.
        self._check_for_ko()

        self._change_turn()

    def _check_if_suicidal(self, x, y):
        """
        Checks if move is suicidal.
        """
        if self.get_num_liberties(x, y) == 0:
            self._pop_history()
            raise ValueError('There are no liberties at that location!')

    def _check_for_ko(self):
        """
        Checks if board state is redundant.
        """
        try:
            if self._array == self._history[-2][0]:
                self._pop_history()
                raise ValueError('Cannot make a redundant move!')
        except IndexError:
            # Insufficient history...let this one slide
            pass

    def _take_pieces(self, x, y):
        """
        Checks if any pieces were taken by the last move at the specified
        coordinates.  If so, removes them from play and tallies resulting
        points.
        """
        scores = []
        for p, (x1, y1) in self._get_surrounding(x, y):
            # If location is opponent's color and has no liberties, tally it up
            if p is self._next_turn and self.get_num_liberties(x1, y1) == 0:
                score = self._kill_group(x1, y1)
                scores.append(score)
                self._tally(score)
        return sum(scores)

    def _change_turn(self):
        self._curr_turn = self._next_turn
        return self._curr_turn

    @property
    def _state(self):
        """
        Returns the game state as a named tuple.
        """
        return self.State(self.copy._array, self._curr_turn, copy(self._scores))

    def _load_state(self, state):
        """
        Loads the specified game state.
        """
        self._array, self._curr_turn, self._scores = state

    def _push_history(self):
        """
        Pushes game state onto history.
        """
        self._history.append(self._state)

    def _pop_history(self):
        """
        Pops and loads game state from history.
        """
        current_state = self._state
        try:
            self._load_state(self._history.pop())
            return current_state
        except IndexError:
            return None

    def _tally(self, score):
        """
        Adds points to the current turn's score.
        """
        self._scores[self._curr_turn] += score

    def _get_none(self, x, y):
        """
        Same thing as Array.__getitem__, but returns None if coordinates are
        not within array dimensions.
        """
        try:
            return self[x, y]
        except ValueError:
            return None

    def _get_surrounding(self, x, y):
        """
        Gets information about the surrounding locations for a specified
        coordinate.  Returns a tuple of the locations clockwise starting from
        the top.
        """
        coords = (
            (x, y - 1),
            (x + 1, y),
            (x, y + 1),
            (x - 1, y),
        )
        return filter(lambda i: bool(i[0]), [
            (self._get_none(a, b), (a, b))
            for a, b in coords
        ])

    def _get_group(self, x, y, traversed):
        """
        Recursively traverses adjacent locations of the same color to find all
        locations which are members of the same group.
        """
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
        """
        Gets the coordinates for all locations which are members of the same
        group as the location at the given coordinates.
        """
        if self[x, y] not in self.TURNS:
            raise ValueError('Can only get group for black or white location')

        return self._get_group(x, y, set())

    def _kill_group(self, x, y):
        """
        Kills a group of black or white pieces and returns its size for
        scoring.
        """
        if self[x, y] not in self.TURNS:
            raise ValueError('Can only kill black or white group')

        group = self.get_group(x, y)
        score = len(group)

        for x1, y1 in group:
            self[x1, y1] = self.EMPTY

        return score

    def _get_liberties(self, x, y, traversed):
        """
        Recursively traverses adjacent locations of the same color to find all
        surrounding liberties for the group at the given coordinates.
        """
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
        """
        Gets the coordinates for liberties surrounding the group at the given
        coordinates.
        """
        return self._get_liberties(x, y, set())

    def get_num_liberties(self, x, y):
        """
        Gets the number of liberties surrounding the group at the given
        coordinates.
        """
        return len(self.get_liberties(x, y))
