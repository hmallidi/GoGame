#!/usr/bin/env python

import argparse
import sys

from go import Board, BoardError, View, clear, getch


def main():
    # Get arguments
    parser = argparse.ArgumentParser(description='Starts a game of go in the terminal.')
    parser.add_argument('-s', '--size', type=int, default=19, help='size of board')

    args = parser.parse_args()

    if args.size < 7 or args.size > 19:
        sys.stdout.write('Board size must be between 7 and 19!\n')
        sys.exit(0)

    # Initialize board and view
    board = Board(args.size)
    view = View(board)
    err = None

    # User actions
    def move():
        """
        Makes a move at the current position of the cursor for the current
        turn.
        """
        board.move(*view.cursor)
        view.redraw()

    def undo():
        """
        Undoes the last move.
        """
        board.undo()
        view.redraw()

    def redo():
        """
        Redoes an undone move.
        """
        board.redo()
        view.redraw()

    def exit():
        """
        Exits the game.
        """
        sys.exit(0)

    # Action keymap
    KEYS = {
        'w': view.cursor_up,
        's': view.cursor_down,
        'a': view.cursor_left,
        'd': view.cursor_right,
        ' ': move,
        'u': undo,
        'r': redo,
        '\x1b': exit,
    }

    # Main loop
    while True:
        # Print board
        clear()
        print('{0}\'s turn...\n'.format(board.turn))
        print('{0}\n'.format(view))
        print('Black\'s Points: {black}\nWhite\'s Points: {white}\n'.
              format(**board.score))

        if err:
            sys.stdout.write('\n' + err + '\n')
            err = None

        # Get action key
        c = getch()

        try:
            # Execute selected action
            KEYS[c]()
        except BoardError as be:
            pass
        except KeyError:
            # Action not found, do nothing
            pass


if __name__ == '__main__':
    main()
