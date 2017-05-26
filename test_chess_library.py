import unittest
import chess.uci
from chess_library import ChessLibrary
from chess_move import ChessMove
from chess_position import ChessPosition
from mock import MagicMock
from concurrent.futures._base import Future
from mock import call

class FakeEngineCommand():
    def result(self):
        test_board = ChessLibrary()
        x = test_board.board.push_uci("e2e4")

        return x, x

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
        command = FakeEngineCommand()
        self.chess_library.engine.go = MagicMock(return_value=command)

        bm = self.chess_library.get_move()

        x = ChessMove(ChessPosition("e", 2), ChessPosition("e", 4))

        self.assertEquals(x.__str__(), bm.__str__())

    def test_set_difficulty(self):
        new_options = {'Skill Level': 5}

        self.chess_library.engine.setoption = MagicMock()
        self.chess_library.set_difficulty(5)

        self.chess_library.engine.setoption.assert_called_with(new_options)

