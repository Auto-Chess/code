import collections
from chess_position import ChessPosition

class LedInterface():

    def __init__(self):
        self.chess_pos = ChessPosition(self, col, row)

    def turn_on_led(self, col, row):
        print("Takes a chess coordinate pair (position) to turn on an LED to show initial position")


    def turn_off_led(self, col, row):
        print("Takes a chess coordinate pair (position) to turn off an LED")


    def start_blinking_led(self, col, row, blink_interval):
        print("Makes the LED start blinking in order to show the user where to move the piece to")


    def stop_blinking_led(self, col, row, blink_interval):
        print("Makes the LED stop blinking")
