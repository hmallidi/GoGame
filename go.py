#!/usr/bin/env python

import argparse
import sys
import platform
import subprocess
import time

from go import Board, View


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
    error = None

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

        black_score, white_score = board.get_score()
        print('Black\'s Points: {}\nWhite\'s Points: {}\n'.format(black_score, 
                                                                  white_score))
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

        print('It is {}\'s turn.\n'.format(board.get_turn_name()))
        print('{}\n'.format(view))

        black_score, white_score = board.get_score()
        print('Black\'s Points: {}\nWhite\'s Points: {}\n'.format(black_score,
                                                                  white_score))

        if error is not None:
            print('\n' + error + '\n')
            error = None

        try:
            print("Input coordinates (0, 0) if you wish to pass the turn. The game ends when both players pass consecutively.\n")
            x = int(input("Please input the x coordinate: "))
            y = int(input("Please input the y coordinate: "))

            if (x == 0 and y == 0):
                PASSED[str(board.get_turn_name())] = True
                time.sleep(1)
                if (PASSED["Black"] is True and PASSED["White"] is True):
                    end_game()
            move(x, y)
            PASSED[str(board.get_turn_name())] = False

        except(KeyError, ValueError) as errorMessage:
            print("\n" + str(errorMessage))
            time.sleep(2)


if __name__ == '__main__':
    main()
