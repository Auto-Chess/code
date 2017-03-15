import collections
from game_loop_entity import GameLoopEntity
"""
Main File, run this file to start Auto Chess.
Run by typing:

    python ./main.py

into your terminal in the directory of this file (main.py).
This tells your computer to run the 'main.py' file with Python on your computer.

Above you see some lines with 'import blablabla'.
These ask Python to include other libraries that are either
included in Python by default or downloaded from the internet.
"""

# Game loop
game_loop = GameLoopEntity()

for i in range(5):
    print()
    print("Round #{}".format(i + 1))
    print("==========")

    # Prompt user for input
    game_loop.prompt_user_for_input()
    initial_pos, final_pos = game_loop.gather_user_input()

    # Give to chess lib
    game_loop.give_to_chess_library(initial_pos, final_pos)

    # Get move
    opp_initial_pos, opp_final_pos = game_loop.get_opponent_move_from_library()

    # Show move
    game_loop.show_opponent_move(opp_initial_pos, opp_final_pos)

print()
print("Game over!")