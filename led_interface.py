import collections
import time
import RPi.GPIO as GPIO
from chess_position import ChessPosition
from chess_move import ChessMove

class LedInterface():

    def __init__(self, operation_mode="hardware"):
        self.operation_mode = operation_mode

        #Sets up the number system for the board and the output pin (location 12 on the diagram)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(12, GPIO.OUT)

    def turn_on_led(self, position):
        if self.operation_mode == "hardware":
            GPIO.output(12, 1)
        else:
            print("LED was turned on")

    def turn_off_led(self, position):
        if self.operation_mode == "hardware":
            GPIO.output(12, 0)
        else:
            print("LED was turned off")

    def start_blinking_led(self, position, blink_interval):
        if self.operation_mode == "hardware":
            for i in range(5)
            GPIO.output(12, 1)
            time.sleep(1)
            GPIO.output(12, 0)
            time.sleep(1)
        else:
            print("LED started blinking")

    def stop_blinking_led(self, position, blink_interval):
        if self.operation_mode == "hardware":
            GPIO.output(12, 0)
        else:
            print("LED stopped blinking")

    def stop_all(self, position):
        if self.operation_mode == "hardware":
            GPIO.output(12, 0)
        else:
            print("All LEDs were turned off")

