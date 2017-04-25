from chess_position import ChessPosition
from led_interface import LedInterface
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
        gettingInitialPosition = True
        while gettingInitialPosition == True:
            initial_input = input("Initial position:")
            initial_col = initial_input[1]
            initial_row = initial_input[0]

            try:
                initial_pos = ChessPosition(initial_col, initial_row)
                gettingInitialPosition = False
            except ValueError as err:
                self.lcd_interface.display("Incorrect coordinate, try again.", "", "")

        gettingFinalPosition = True
        while gettingFinalPosition == True:
            final_input = input("Final position:")
            final_col = final_input[1]
            final_row = final_input[0]

            try:
                final_pos = ChessPosition(final_col, final_row)
                gettingFinalPosition = False
            except ValueError as err:
                self.lcd_interface.display("Incorrect coordinate, try again.", "", "")

        move = ChessMove(initial_pos, final_pos)
        return move

    def give_to_chess_library(self,initial_pos, final_pos):
        try:
            chessMove = ChessMove(initial_pos, final_pos)
            self.chess_library.handOff("","")
            #TODO when chess library class is made

        except ValueError as err:
            # Or catch whatever error type the 3rd party API throws
            self.lcd_interface.display("The 3rd party library was unable to receive input.", "", "")


    def get_opponent_move_from_library(self):
        opponentMove = self.chess_library.getMove()

        return opponentMove

    def show_opponent_move(self,initial_pos, final_pos):
        self.led_interface.turn_on_led(initial_pos)
        self.led_interface.start_blinking_led(final_pos)
