import unittest
from chess_library import ChessLibrary
from game_loop_entity import GameLoopEntity
from chess_position import ChessPosition
from chess_move import ChessMove
from led_interface import LedInterface
from mock import MagicMock
from mock import patch
from mock import call

class TestLCDInerface(unittest.TestCase):
    def test_display(self):
        self.assertEquals(True,True)

if len(first_line) > 16:
    raise ValueError("First line of text can not be more than 16 characters")

if len(second_line) > 16:
    raise ValueError("First line of text can not be more than 16 characters")