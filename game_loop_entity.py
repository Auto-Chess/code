from chess_position import ChessPosition
from led_interface import LedInterface
from chess_move import ChessMove
from lcd_interface import LCDInterface
from chess_library import ChessLibrary

from webserver_interface import WebServerInterface

try:
    from pynput import keyboard
except Exception as e:
    keyboard = False

from threading import Thread

"""Game loop entity class
Return:
    -str: Asks user for initial input
    -int: Gives user input to chess engine
    -int: Retrieves the opponent move from the chess engine
    -str: Shows opponent move on led board
"""
class GameLoopEntity():

    def __init__(self):
        self.paused = False
        self.welcomed = False
        self.lcd_interface = LCDInterface()
        self.chess_library = ChessLibrary()
        self.chess_library.set_difficulty(2)
        self.led_interface = LedInterface()
        self.webserver_interface = WebServerInterface()
        self.webserver_interface.register()
        self.thread = Thread(target=self.start_listening)
        self.thread.start()
        self.listener = None

    """ Listens for the keyboard to begin typing.
        Return:
            -str: Keyboard is not imported
    """

    def start_listening(self):
        if keyboard != False:
            # Collect events until released
            self.listener = keyboard.Listener(
                    on_press=self.on_press,
                    on_release=self.on_release)
        else:
            print ("start_listening: KEYBOARD NOT IMPORTED")

    def stop_listening(self):
        if self.listener is None:
            print("Not listening")
        else:
            self.listener.stop()
            self.listener.join()
            self.thread.join()

    """Listens for when key is being pressed.
        Dif asks for in int input of desired difficulty for game
        If Q is pressed the quit game option runs
        If N is pressed the new game option runs
        Arg:
            -key(str): Which key is being pressed

        Returns:
            -str: Tells user to enter difficulty
            -int: Number for difficulty is passed to engine

        Raises:
            -Attribute Error: If esc key is pressed a pause menu will appear
    """

    def on_press(self, key):
        try:
            print('alphanumeric key {0} pressed'.format(key.char))
            if self.paused:
                if key.char == 'd':
                    self.lcd_interface.display("Enter Difficulty 0-20", "")
                    dif = input()
                    dif = dif[1:len(dif)]
                    self.chess_library.set_difficulty(int(dif))
                    self.chess_library.get_difficulty()
                elif key.char == 'n':
                    self.chess_library.start_game
                    self.webserver_interface.signal_game_over
                elif key.char == 'q':
                    self.webserver_interface.signal_game_over
                    self.welcomed = False
        except AttributeError:
            'special key {0} pressed'.format(key)
            if key == keyboard.Key.esc:
                self.paused = True

    """Listens for when a button is released
        Arg:
            -key(str): Which key is being pressed

        Returns:
            Bool: Turns false to stop listener
    """

    def on_release(self, key):
        '{0} released'.format(
            key)
        if self.chess_library.is_game_over():
            # Stop listener
            return False

    """Sends a string of instructions to the LCD display
        Returns:
            -str: Welcome user to the game
            -str: Tells user to give their input
    """

    def prompt_user_for_input(self):
        if not self.welcomed:
            self.welcomed = True
            self.lcd_interface.display("Welcome to Auto Chess", "")
        self.lcd_interface.display("Enter initial then final position: ", "")

    """ Gathers the user input by taking in an initial position and final position
        Each position is make of an initial column and initial row
        and an final column and final row
        Creates a chess position from the initial column and initial row
        does the same for the final position.
        Creates a move from the initial and final position
        Returns:
            -str: Asks user for initial position
            -str: Asks user for final position
            -str: Chess move

       Raises:
            -ValueError: If an incorrect initial coordinate is entered the value will raise
            -ValueError: If an incorrect final coordinate is entered the value will raise
    """

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

    """ Gives the inputted initial and final position to the chess engine.
        Creates a chessMove from the positions.
        Sends the chess move to the webserver interface.
        Args:
            initial_pos(str): The given input in previous method
            final_pos(str): The given input in previous method
    """

    def give_to_chess_library(self, initial_pos, final_pos):
        chessMove = ChessMove(initial_pos, final_pos)
        self.chess_library.hand_off(chessMove)
        self.webserver_interface.push_player_move(chessMove)
        #TODO when chess library class is made

    """ Takes the opponent move from the chess engine.
        Pushes opponent move to webserver.
        Returns:
            -int: Opponent move from chess engine
    """

    def get_opponent_move_from_library(self):
        opponentMove = self.chess_library.get_move()
        self.webserver_interface.push_opponent_move(opponentMove)
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
        self.webserver_interface.register
        i = 1
        while not self.chess_library.is_game_over():
            print()
            print("Round #{}".format(i + 1))
            print("==========")

            # Prompt user for input
            self.prompt_user_for_input()
            user_move = self.gather_user_input()
            self.led_interface.stop_all()

            # Give to chess lib
            self.give_to_chess_library(user_move.init_pos, user_move.final_pos)

            # Get move
            opp_move = self.get_opponent_move_from_library()

            # Show move
            self.show_opponent_move(opp_move.init_pos, opp_move.final_pos)

        self.webserver_interface.signal_game_over()