class GameLoopEntity():
    def __init__(self):
        self.welcomed = False
        pass
    def prompt_user_for_input(self):
        if self.welcomed == False:
            self.welcomed = True
            print("Welcome to Auto Chess")
        print('Enter inital and final position: ')

    def gather_user_input(self):
        usrInpt = input()
        return usrInpt

        return "Fake user initial position", "Fake user final position"

    def give_to_chess_library(self,initial_pos, final_pos):
        print("give_to_chess_library")
        print("=================================")
        print("initial_pos is where the piece was.")
        print("final_pos is the new position of the piece.")
        print("1. Give this information to the third party chess library.")
        print("2. If anything goes wrong return an error, otherwise return nothing")
        try:
            # third_party_library_input(initial_pos, final_pos)
            # Remove pass when ready (obviously)
            pass
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