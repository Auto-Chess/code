# Importing the necessary libraries to run the tests
import unittest
from chess_library import ChessLibrary
from game_loop_entity import GameLoopEntity
from chess_position import ChessPosition
from chess_move import ChessMove
from lcd_interface import LCDInterface
from led_interface import LedInterface
from mock import MagicMock
from mock import patch
from mock import call

# Creating the test class with the testing methods
class TestLCDInterface(unittest.TestCase):

    # Setting up a variable to use the variables in the other libraries
    def setUp(self):
        self.lcdInterface = LCDInterface("test")

    # Testing the first line of the LCD Display
    def test_display_first_line(self):
        first_line = "aklsjd;bfoasjng;oasjnjf;oasund;absdgjkasb.dkjgbas;dfjka;js"
        second_line = "Hello"
        self.lcdInterface.display(first_line, second_line)
        with self.assertRaises(ValueError) as context:
            self.lcdInterface.display(first_line, second_line)

    #Testing the second line of the LCD Display
    def test_display_second_line(self, top_checker, bottom_checker):
        first_line = "Hello"
        second_line = "aa;lskdfn;alksdnf;asdh;flaksdf;oasdhf;aiszdhf;alnsdkjfj;alsdf;j"
        self.lcdInterface.display(first_line, second_line)
        with self.assertRaises(ValueError) as context:
            self.lcdInterface.display(first_line, second_line)

    #Checking for Success; that the text has successfully displayed
    def test_display_success(self):
        self.lcdInterface.lcdCom.write = MagicMock()
        first_line = "Hello"
        second_line = "World"
        self.lcdInterface.display(first_line, second_line)

        self.lcdInterface.lcdCom.write.assert_has_calls(call(b"\xFE\x01"), call(first_line), call(b"\xFE\xC0"), call(second_line))