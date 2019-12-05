#!/usr/bin/env python

import argparse
import sys

from go import Board, BoardError, View, clear, getch


def main():
    print("We are going to play a game of Go.")

    board_size = 0

    while(board_size != 9 and board_size != 13 and board_size != 19):
        try:
            board_size = int(input("Please input a board size (9, 13, 19): "))
        except ValueError:
            pass

    # Initialize board and view
    board = Board(board_size)
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
