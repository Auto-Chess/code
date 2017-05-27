from game_loop_entity import GameLoopEntity
import webserver
"""
Main File, run this file to start Auto Chess.
Run by typing:

    python ./main.py

into your terminal in the directory of this file (main.py).
This tells your computer to run the 'main.py' file with Python on your computer.
"""

# Game loop
game_loop = GameLoopEntity()

webserver.run_webserver_in_thread()

try:
    game_loop.run()
except KeyboardInterrupt as e:
    webserver.stop_webserver_in_thread()