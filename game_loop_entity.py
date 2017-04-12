from chess_move import ChessMove
from lcd_interface import LCDInterface
class GameLoopEntity():
    def __init__(self):
        self.welcomed = False
        self.lcd_interface = LCDInterface()

    def prompt_user_for_input(self):
        if self.welcomed == False:
            self.welcomed = True
            self.lcd_interface.display("Welcome to Auto Chess","","")
        self.lcd_interface.display("Enter initial then final position: ")

    def gather_user_input(self):
        initial = input("Initial position:")
        final = input("Final position:")
        return initial, final

    def give_to_chess_library(self,initial_pos, final_pos):
        try:
            # third_party_library_input(initial_pos, final_pos)
            # Remove pass when ready (obviously)
            print("Here we would give library move: \"{}\" => \"{}\"".format(initial_pos, final_pos))
        except ValueError as err:
            # Or catch whatever error type the 3rd party API throws
            print("The 3rd party library was unable to receive input.")
        print("")

    def get_opponent_move_from_library(self):
        print("Here is where the third party chess interface would ask the third party chess library for the oppponent's move")
        print("Opponent's move will then be given to the third party chess interface")

        return "Fake opponent initial move", "Fake opponent final move"

    def show_opponent_move(self,initial_pos, final_pos):
        print("Opponent move \"{}\" => \"{}\"".format(initial_pos, final_pos))