#!/usr/bin/env python

import argparse
import sys
import platform
import subprocess
import time

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

    def end_game():
        """
        Exits the game.
        """
        clear()
        print('Black\'s Points: {black}\nWhite\'s Points: {white}\n'.
              format(**board.score))
        print("\nThe game has ended.")
        time.sleep(5)
        sys.exit(0)

    PASSED = {
            "Black": False,
            "White": False
    }

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
            print("Input coordinates (0, 0) if you wish to pass the turn. The game ends when both players pass consecutively.\n")
            x = int(input("Please input the x coordinate: "))
            y = int(input("Please input the y coordinate: "))

            if (x == 0 and y == 0):
                PASSED[str(board.turn)] = True
                time.sleep(1)
                if (PASSED["Black"] is True and PASSED["White"] is True):
                    end_game()
            move(x, y)
            PASSED[str(board.turn)] = False

        except(BoardError, KeyError, ValueError) as error:
            print("\n" + str(error))
            time.sleep(2)


if __name__ == '__main__':
    main()
