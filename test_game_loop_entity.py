import unittest
from chess_library import ChessLibrary
from game_loop_entity import GameLoopEntity
from chess_position import ChessPosition
from chess_move import ChessMove
from mock import MagicMock
from mock import patch


class TestGiveToChessLibrary(unittest.TestCase):
    def setUp(self):
        self.chess_library = ChessLibrary()
        self.game_loop = GameLoopEntity()


    @patch("chess_library.ChessLibrary.handOff")
    def test_chess_library_handOff(self,fn):
        initial_pos = ChessPosition("b",4)
        final_pos = ChessPosition("c",1)
        chessMove = ChessMove(initial_pos, final_pos)
        self.game_loop.give_to_chess_library(initial_pos, final_pos)

        fn.assert_called_once_with(chessMove)

if __name__ == '__main__':
    unittest.main()