from chess_position import ChessPosition
from led_interface import LedInterface
from chess_move import ChessMove
from lcd_interface import LCDInterface
from chess_library import ChessLibrary
import time
from getch import getch

from webserver_interface import WebServerInterface


"""Game loop entity class
Return:
    -str: Asks user for initial input
    -int: Gives user input to chess engine
    -int: Retrieves the opponent move from the chess engine
    -str: Shows opponent move on led board
"""
class GameLoopEntity():

    def __init__(self, operation_mode):
        self.welcomed = False
        self.pressed = False
        self.new_game_on_exit = False
        self.operation_mode = operation_mode

        self.lcd_interface = LCDInterface(self.operation_mode)
        self.chess_library = ChessLibrary()
        self.chess_library.set_difficulty(0)
        self.led_interface = LedInterface([9, 11, 5, 6, 13, 19, 26, 21], [2, 3, 4, 17, 27, 22, 10, 20], self.operation_mode)
        self.led_interface.setup()
        self.led_interface.start_run_in_thread()

        self.webserver_interface = WebServerInterface("http://autochess.noahhuppert.com")


    """Gets user input and displays it on lcd as they type
    Args:
        - first_line (str): First line of text to display on lcd
        - second_line (str): Second line of text to display before user input
    
    Returns:
        - str: User inputted string
    """
    def lcd_input(self, first_line, second_line):
        user_input = ""
        latest = None
        while latest != repr("\r"):
            latest = repr(getch())
            if latest == repr("\r"):# Return
                break
            elif latest == repr("\x7f"):# Backspace
                user_input = user_input[:-1]
            elif latest == repr("\x03"):#Ctrl+c
                self.close()
                exit()
            else:
                user_input += str(latest[1:-1])

            to_display = user_input
            while True:
                try:
                    self.lcd_interface.display(first_line, "{}: {}".format(second_line, str(to_display)))
                    break
                except ValueError:
                    to_display = to_display[1:]
        return user_input

    """ Listens for the keyboard to begin typing.
        Saves listener for later usage.
        Return:
            -str: Keyboard is not imported
    """

    def pause(self):
        self.lcd_interface.display("Paused", "d, n, or q")
        user_input = self.lcd_input("Paused", "d, n, or q")
        if user_input == 'd':
            self.lcd_interface.display("Enter Diff. 0-20", "")
            dif = self.lcd_input("Enter Diff. 0-20", "New diff.")
            dif = dif[-1:]
            self.chess_library.set_difficulty(int(dif))
            self.chess_library.get_difficulty()
        elif user_input == 'n':
            self.lcd_interface.display("New game", "")
            res = self.webserver_interface.signal_game_over()
            if res is not None:
                print("Error signalling game over: {}".format(res))
            self.new_game_on_exit = True
            input()
            self.close()

        elif user_input == 'q':
            self.lcd_interface.display("Quit", "")
            res = self.webserver_interface.signal_game_over()
            if res is not None:
                print("Error signalling game over: {}".format(res))
            else:
                self.close()
                exit()

            self.welcomed = False

    """
    Sends a string of instructions to the LCD display
    Takes the initial and final position after calling gather_user_input twice
    Treates and returns a chessmove from the positions
        Returns:
            -str: Welcome user to the game
            -str: Tells user to give their input
    """

    def prompt_user_for_input(self):
        if not self.welcomed:
            self.welcomed = True
            self.lcd_interface.display("Welcome to Auto", "Chess")

        initial_pos = self.gather_user_input("Initial")
        final_pos = self.gather_user_input("Final")

        if self.new_game_on_exit:
            return

        move = ChessMove(initial_pos, final_pos)

        return move

    """ Gathers the user input by taking in an position
        Each position is made of an column and row
        Creates a chess position from the column and row
        Returns:
            -str: Asks user for initial position
            -str: Asks user for final position
            -str: Chess move

       Raises:
            -ValueError: If an incorrect coordinate is entered the value will raise

    """
    def gather_user_input(self, prompt):
        while not self.new_game_on_exit:
            while True:
                self.lcd_interface.display(prompt, "position")
                user_input = self.lcd_input(prompt, "position")

                if user_input == "pause":
                    self.pause()
                    if self.new_game_on_exit:
                        return
                else:
                    break
            try:
                col = user_input[0]
                row = int(user_input[1])

                position = ChessPosition(col, row)
                return position
            except ValueError:
                self.lcd_interface.display("Bad move", "Try again")
                input()
            except IndexError:
                self.lcd_interface.display("Bad move", "Try again")
                input()

    """ Gives the inputted initial and final position to the chess engine.
        Creates a chessMove from the positions.
        Sends the chess move to the webserver interface.
        Args:
            initial_pos(str): The given input in previous method
            final_pos(str): The given input in previous method
    """

    def give_to_chess_library(self, move):
        self.chess_library.hand_off(move)
        errs = self.webserver_interface.push_player_move(move)
        if errs is not None:
            print("Game Loop Entity: Failed to push player move to website: {}".format(errs))

    """ Takes the opponent move from the chess engine.
        Pushes opponent move to webserver.
        Returns:
            -int: Opponent move from chess engine
    """

    def get_opponent_move_from_library(self):
        opponentMove = self.chess_library.get_move()
        errs = self.webserver_interface.push_opponent_move(opponentMove)
        if errs is not None:
            print("Game Loop Entity: Failed to push opponent move to website: {}".format(errs))
        return opponentMove

    """Sends the opponent move the LED board.
        Args:
            initial_pos(str): The opponents initial position
            final_pos(str): The opponents final position
    """

    def show_opponent_move(self, initial_pos, final_pos):
        self.led_interface.turn_on_led(initial_pos)
        self.led_interface.start_blinking_led(final_pos, 1)

    """ Runs the game loop entity.
        Checks if game loop is in a game over stage.
        Prompts the user for input
        Gives the initial and final position to gather user input method
        Send the initial position and final position to the chess library
        Gets the opponents initial and final position from the chess engine
        Shows the opponents move on the LED board.
        Loops until game is said to be over.
        Sends game termination to the web server.
        Returns:
            -str: Tells user the numbered round in the game
    """

    def run(self):
        errs = self.webserver_interface.register()
        if errs is not None:
            print("Game Loop Entity: Failed to register chess board {}".format(errs))
        else:
            self.lcd_interface.display("Website code", self.webserver_interface.chess_board_short_code)
            input()

        i = 1
        while not self.chess_library.is_game_over() and not self.new_game_on_exit:
            while True:
                # Prompt user for input
                user_move = self.prompt_user_for_input()

                if self.new_game_on_exit:
                    return

                try:
                    # Give to chess lib
                    self.give_to_chess_library(user_move)
                    break
                except ValueError as e:
                    self.lcd_interface.display("Bad move", "Try again")

            # Get move
            opp_move = self.get_opponent_move_from_library()

            # Show move
            self.show_opponent_move(opp_move.init_pos, opp_move.final_pos)
            self.lcd_interface.display("Move opp.", "piece")
            input()
            self.led_interface.stop_all()

        if not self.new_game_on_exit:
            errs = self.webserver_interface.signal_game_over()
            if errs is not None:
                print("Game Loop Entity: Failed to signal game over: {}".format(errs))

    def close(self):
        self.led_interface.running = False
        self.led_interface.thread.join()

        self.led_interface.cleanup()
