from chess_position import ChessPosition
from led_interface import LedInterface
from chess_move import ChessMove
from lcd_interface import LCDInterface
from chess_library import ChessLibrary


class GameLoopEntity():
    def __init__(self):
        self.welcomed = False
        self.lcd_interface = LCDInterface()
        self.chess_library = ChessLibrary()
        self.led_interface = LedInterface()

    def prompt_user_for_input(self):
        if not self.welcomed:
            self.welcomed = True
            self.lcd_interface.display("Welcome to Auto Chess","")
        self.lcd_interface.display("Enter initial then final position: ","")

    def gather_user_input(self):
        initial_pos = None
        final_pos = None
        getting_initial_position = True
        while getting_initial_position:
            initial_input = input("Initial position:")
            initial_col = initial_input[0]
            initial_row = int(initial_input[1])

            try:
                initial_pos = ChessPosition(initial_col, initial_row)
                getting_initial_position = False
            except ValueError:
                self.lcd_interface.display("Incorrect initial coordinate, try again.", "")

        getting_final_position = True
        while getting_final_position:
            final_input = input("Final position:")
            final_col = final_input[0]
            final_row = int(final_input[1])

            try:
                final_pos = ChessPosition(final_col, final_row)
                getting_final_position = False
            except ValueError as err:
                self.lcd_interface.display("Incorrect final coordinate, try again.", "")

        move = ChessMove(initial_pos, final_pos)
        return move

    def give_to_chess_library(self, initial_pos, final_pos):
        chess_move = ChessMove(initial_pos, final_pos)
        self.chess_library.hand_off(chess_move)
        # TODO when chess library class is made

    def get_opponent_move_from_library(self):
        opponent_move = self.chess_library.get_move()
        return opponent_move

    def show_opponent_move(self,initial_pos, final_pos):
        self.led_interface.turn_on_led(initial_pos)
        self.led_interface.start_blinking_led(final_pos,1)
        
    def run(self):
        while not self.chess_library.is_game_over():
            print()
            print("Round #{}".format(i + 1))
            print("==========")

            # Prompt user for input
            self.prompt_user_for_input()
            initial_pos, final_pos = self.gather_user_input()
            self.led_interface.stop_all()

            # Give to chess lib
            self.give_to_chess_library(initial_pos, final_pos)

            # Get move
            opp_initial_pos, opp_final_pos = self.get_opponent_move_from_library()

            # Show move
            self.show_opponent_move(opp_initial_pos, opp_final_pos)
