from game_loop_entity import GameLoopEntity
"""
Main File, run this file to start Auto Chess.
Run by typing:

    python ./main.py

into your terminal in the directory of this file (main.py).
This tells your computer to run the 'main.py' file with Python on your computer.
"""

# Game loop
game_loop = GameLoopEntity()

try:
    game_loop.run()
except KeyboardInterrupt as e:
    game_loop.led_interface.running = False
    game_loop.led_interface.cleanup()
    game_loop.led_interface.thread.join()
