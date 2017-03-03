"""
Main File, run this file to start Auto Chess
"""


def prompt_user_for_input():
    print("This function prompts the user on the screen to input their move.")


def gather_user_input():
    print("This function takes the values entered from user and hands them off to the Give To Chess Library function.")


def give_to_chess_library():
    print("1. Locate where the initial position of the piece was.")
    print("2. Locate the new position of the piece.")
    print("3. Give this information to the third party chess library.")


def get_opponent_move_from_library():
    print("The third party chess library will receive a request from the third party chess interface.")
    print("The third party chess library will then give the opponents move to the third party chess interface.")


def show_opponent_move():
    print("1. Hand Initial and Final Piece Positions to LED Interface.")
    print("2. Hand Initial and Final Piece Positions to LCD text display interface")

prompt_user_for_input()

gather_user_input()

give_to_chess_library()

get_opponent_move_from_library()

show_opponent_move()