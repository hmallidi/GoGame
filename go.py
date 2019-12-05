#!/usr/bin/env python

import argparse
import sys
import platform
import subprocess

from go import Board, BoardError, View


def clear():
    subprocess.check_call('cls' if platform.system() == 'Windows' else 'clear', shell=True)


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
    def move(x,  y):
        """
        Makes a move at the given coordinates.
        """
        board.move(x, y)
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

    # Main loop
    while True:
        clear()

        print('{0}\'s turn...\n'.format(board.turn))
        print('{0}\n'.format(view))
        print('Black\'s Points: {black}\nWhite\'s Points: {white}\n'.
              format(**board.score))

        if err:
            sys.stdout.write('\n' + err + '\n')
            err = None

        try:
            x = int(input("Please input the x coordinate: "))
            y = int(input("Please input the y coordinate: "))

            move(x, y)
        except BoardError:
            pass
        except KeyError:
            pass
        except ValueError:
            pass


if __name__ == '__main__':
    main()
