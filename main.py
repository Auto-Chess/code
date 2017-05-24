from game_loop_entity import GameLoopEntity
import webserver
"""
Main File, run this file to start Auto Chess.
Run by typing:

    python ./main.py

into your terminal in the directory of this file (main.py).
This tells your computer to run the 'main.py' file with Python on your computer.
"""

# Webserver
webserver.run_webserver_in_thread()

# Game loop
game_loop = GameLoopEntity()
game_loop.run()