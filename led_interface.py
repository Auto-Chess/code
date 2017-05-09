import collections
import time
import RPi.GPIO as GPIO
from chess_position import ChessPosition
from chess_move import ChessMove

class LedInterface():

    def __init__(self):
       pass

    #Sets up the number system for the board and the output pin (location 12 on the diagram)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(12, GPIO.OUT)

    def turn_on_led(self, position):
        GPIO.output(12, 1)

    def turn_off_led(self, position):
        GPIO.output(12, 0)

    def start_blinking_led(self, position, blink_interval):
        for i in range(5)
            GPIO.output(12, 1)
            time.sleep(1)
            GPIO.output(12, 0)
            time.sleep

    def stop_blinking_led(self, position, blink_interval):
        GPIO.output(12, 0)

    def stop_all(self, position):
        GPIO.output(12, 0)

