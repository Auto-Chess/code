import unittest
import chess.uci
from chess_library import ChessLibrary
from mock import MagicMock
from mock import patch
from mock import call


class TestChessLibrary(unittest.TestCase):
    def setUp(self):
        self.chess_library = ChessLibrary()

