#!/usr/bin/env python

import argparse
import sys
import platform
import subprocess
import time

from go_game import GoGame


def clear():
    subprocess.check_call('cls' if platform.system() == 'Windows' else 'clear',
                          shell=True)


def main():
    print("We are going to play a game of Go.")

    board_size = 0

    while(board_size != 9 and board_size != 13 and board_size != 19):
        try:
            board_size = int(input("Please input a board size (9, 13, 19): "))
        except ValueError:
            pass

    game = GoGame(board_size)
    error = None

    def end_game():
        clear()

        (black_stones_on_board,
         white_stones_on_board) = game.get_num_stones_on_board()

        print('Black had {} stones on the board at the end of the game.\n'.
              format(black_stones_on_board))
        print('White had {} stones on the board at the end of the game.\n'.
              format(white_stones_on_board))

        if black_stones_on_board < white_stones_on_board:
            print("\n\nWhite has won!\n\n")
        elif black_stones_on_board > white_stones_on_board:
            print("\n\nBlack has won!\n\n")
        else:
            print("\n\nBlack and White have tied.")

        print("\nThe game has ended.")
        time.sleep(5)
        sys.exit(0)

    PASSED = {
            "Black": False,
            "White": False
    }

    while True:
        clear()

        print('It is {}\'s turn.\n'.format(game.get_turn_name()))
        print('{}\n\n'.format(game.get_board_display()))

        (black_stones_captured,
         white_stones_captured) = game.get_stones_captured()
        (black_stones_on_board,
         white_stones_on_board) = game.get_num_stones_on_board()

        print('Black has captured {} stones.\n'.format(black_stones_captured))
        print('White has captured {} stones.\n'.format(white_stones_captured))

        print('Black has {} stones on the board.\n'.
              format(black_stones_on_board))
        print('White has {} stones on the board.\n\n'.
              format(white_stones_on_board))

        if error is not None:
            print('\n' + error + '\n')
            error = None

        try:
            print("Input coordinates (0, 0) if you wish to pass the turn." +
                  "The game ends when both players pass consecutively.\n")
            print("The winner of the game is whoever has the most stones on" +
                  "the board at the end.\n\n")
            x = int(input("Please input the x coordinate: "))
            y = int(input("Please input the y coordinate: "))

            if (x == 0 and y == 0):
                PASSED[str(game.get_turn_name())] = True
                time.sleep(1)
                if (PASSED["Black"] is True and PASSED["White"] is True):
                    end_game()
            game.move(x, y)
            PASSED[str(game.get_turn_name())] = False

        except(KeyError, ValueError) as errorMessage:
            print("\n" + str(errorMessage))
            time.sleep(2)


if __name__ == "__main__":
    main()
