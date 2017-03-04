import collections
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

def prompt_user_for_input():
    print("prompt_user_for_input")
    print("=================================")
    print("This function prompts the user on the screen to input their move.")
    print("This is done by handing some text which asks the user to the LCD text display interface")
    print("")


def gather_user_input():
    print("gather_user_input")
    print("=================================")
    print("This function gets the user entered initial and final piece positions and returns them")
    print("")

    return "Fake user initial position", "Fake user final position"

def give_to_chess_library(initial_pos, final_pos):
    print("give_to_chess_library")
    print("=================================")
    print("initial_pos is where the piece was.")
    print("final_pos is the new position of the piece.")
    print("1. Give this information to the third party chess library.")
    print("2. If anything goes wrong return an error, otherwise return nothing")
    print("")

def get_opponent_move_from_library():
    print("get_opponent_move_from_library")
    print("=================================")
    print("1. Use third party chess interface to ask third party Chess library for opponent's move")
    print("2. Opponent's move will be given to third party Chess interface")
    print("3. This function should return the Opponent's initial and final move")
    print("")

    return "Fake opponent initial move", "Fake opponent final move"

def show_opponent_move(initial_pos, final_pos):
    print("show_opponent_move")
    print("=================================")
    print("1. Hand Initial and Final Piece Positions to LED Interface.")
    print("2. Hand Initial and Final Piece Positions to LCD text display interface")
    print("")


"""
Now that we have defined all our functions above we are going to
call them in the order defined in the Game Loop entity
"""
# Prompt user for input
prompt_user_for_input()
initial_pos, final_pos = gather_user_input()

# Give to chess lib
give_to_chess_library(initial_pos, final_pos)

# Get move
opp_initial_pos, opp_final_pos = get_opponent_move_from_library()

# Show move
show_opponent_move(opp_initial_pos, opp_final_pos)