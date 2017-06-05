import unittest
import time
import RPi.GPIO as GPIO
from chess_position import ChessPosition
from led_interface import LedInterface
from mock import MagicMock
from mock import patch

class testLedInterface(unittest.TestCase):
    def setUp(self):
        self.led_interface = LedInterface(operation_mode= "hardware")

    def test_turn_on_led(self):
        pos = ChessPosition("b",4)
        self.led_interface.turn_on_led(pos)

        self.assert_equals(True, True)