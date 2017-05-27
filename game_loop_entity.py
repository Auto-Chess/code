from chess_position import ChessPosition
from led_interface import LedInterface
from chess_move import ChessMove
from lcd_interface import LCDInterface
from chess_library import ChessLibrary

from webserver_interface import WebServerInterface
from pynput import keyboard
from threading import Thread


class GameLoopEntity():

    def __init__(self):
        self.paused = False
        self.welcomed = False
        self.lcd_interface = LCDInterface()
        self.chess_library = ChessLibrary()
        self.led_interface = LedInterface()
        self.webserver_interface = WebServerInterface()
        self.webserver_interface.register()
        self.thread = Thread(target=self.start_listening)
        self.thread.start()

    def start_listening(self):
        # Collect events until released
        with keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()

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

    def on_release(self, key):
        '{0} released'.format(
            key)
        if self.chess_library.is_game_over():
            # Stop listener
            return False

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

    def give_to_chess_library(self,initial_pos, final_pos):
        chessMove = ChessMove(initial_pos, final_pos)
        self.chess_library.hand_off(chessMove)
        self.webserver_interface.push_player_move(chessMove)
        #TODO when chess library class is made

    def get_opponent_move_from_library(self):
        opponentMove = self.chess_library.get_move()
        self.webserver_interface.push_opponent_move()
        return opponentMove

    def show_opponent_move(self,initial_pos, final_pos):
        self.led_interface.turn_on_led(initial_pos)
        self.led_interface.start_blinking_led(final_pos,1)
        
    def run(self):
        self.webserver_interface.register
        i = 1
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

        self.webserver_interface.signal_game_over


