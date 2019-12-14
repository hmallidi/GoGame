Group Members:
Harinadha Reddy Mallidi
Preeti Arumalla

---------------------------------------
How to run the project:
In terminal, input the following line

python go_main.py
---------------------------------------

This project is a Python version of the classic game of Go, which was invented in China.
The game is known to very complex, and is also the oldest board game still played today.


Rules of our game:

There are 2 players that play on a 9x9, 13x13, or 19x19 board. 
Black makes the first move, after which Black and White alternate.

To make a move, a player must play a stone on an empty intersection on the board.

A stone or a group of stones are captured if all of the intersections directly adjacent to the group
are occupied by the opposing player.

Each player can choose to pass their turn at any time.
The game ends when both players pass their turn consecutively.

Whoever has the most stones on the board at the end of the game wins (We used the Stone Scoring System).

Illegal moves include:
    A player placing a stone at a place where, if placed, would cause the same player to forfeit their stone
    or a group of stones to another player (This is considered as a SUICIDE move)

    A player cannot make a move that is redundant, or that would cause the board to go back to an immediately
    previous state. This is prevented because if this were allowed, two players could decide to alternate between
    playing the same moves over and over again, causing no progress in the game (This is the KO rule)

    A player can't play a stone on an intersection that already has a stone or is outside of the board boundaries.


This video explains the rules of the game well (and it isn't a 15 minute video fortunately):
https://www.youtube.com/watch?v=5PTXdR8hLlQ

The only difference between these rules and our rules is that the video explains Go using the Komi Scoring System,
whereas our game uses the Stone Scoring System. 

