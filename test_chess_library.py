import unittest
import chess.uci
from chess_library import ChessLibrary
from chess_move import ChessMove
from chess_position import ChessPosition
from mock import MagicMock
from mock import call


class TestChessLibrary(unittest.TestCase):
    def setUp(self):
        self.chess_library = ChessLibrary()


    def test_hand_off(self):
        initial = ChessPosition("e", 2)
        final = ChessPosition("e", 4)
        move = ChessMove(initial, final)

        self.chess_library.board.push_uci = MagicMock()
        self.chess_library.engine.position = MagicMock()

        self.chess_library.hand_off(move)

        self.chess_library.board.push_uci.assert_called_with(move.__str__())
        self.chess_library.engine.position.assert_called_with(self.chess_library.board)

    def test_get_move(self):
        self.chess_library.engine.go = MagicMock(return_value=chess.Move)