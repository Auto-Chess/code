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
    print("Welcome to Auto Chess")
    print('Enter inital and final position: ')


def gather_user_input():
    usrInpt = input()
    return usrInpt

    return "Fake user initial position", "Fake user final position"

	
def give_to_chess_library(initial_pos, final_pos):
    print("give_to_chess_library")
    print("=================================")
    print("initial_pos is where the piece was.")
    print("final_pos is the new position of the piece.")
    print("1. Give this information to the third party chess library.")
    print("2. If anything goes wrong return an error, otherwise return nothing")
    try:
        #third_party_library_input(initial_pos, final_pos)
		#Remove pass when ready (obviously)
        pass
    except ValueError as err:
        #Or catch whatever error type the 3rd party API throws
        print("The 3rd party library was unable to receive input.")
    print("")


def get_opponent_move_from_library():
    print("Here is where the third party chess interface would ask the third party chess library for the oppponent's move")
    print("Opponent's move will then be given to the third party chess interface")

    return "Fake opponent initial move", "Fake opponent final move"

def show_opponent_move(initial_pos, final_pos):
    print("Opponent move \"{}\" => \'{}\"".format(initial_pos, final_pos))

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
