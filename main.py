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
game_loop = GameLoopEntity(operation_mode)

try:
    game_loop.run()
except KeyboardInterrupt as e:
    game_loop.close()
