from game_loop_entity import GameLoopEntity
import os

"""
Main File, run this file to start Auto Chess.
Run by typing:

    python ./main.py

into your terminal in the directory of this file (main.py).
This tells your computer to run the 'main.py' file with Python on your computer.
"""

# Game loop
operation_mode = os.getenv("OP_MODE", "software")
while True:
    game_loop = GameLoopEntity(operation_mode)

    try:
        game_loop.run()
        if not game_loop.new_game_on_exit:
            break
    except KeyboardInterrupt as e:
        game_loop.close()
