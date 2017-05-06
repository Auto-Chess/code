import unittest
from chess_library import ChessLibrary
from game_loop_entity import GameLoopEntity
from chess_position import ChessPosition
from chess_move import ChessMove
from led_interface import LedInterface
from mock import MagicMock
from mock import patch

class TestGameLoopEntity(unittest.TestCase):
    def setUp(self):
        self.chess_library = ChessLibrary()
        self.game_loop = GameLoopEntity()
        self.led_interface = LedInterface()

    @patch("chess_library.ChessLibrary.handOff")
    def test_give_to_chess_library(self,fn):
        initial_pos = ChessPosition("b",4)
        final_pos = ChessPosition("c",1)
        chessMove = ChessMove(initial_pos, final_pos)
        self.game_loop.give_to_chess_library(initial_pos, final_pos)

        fn.assert_called_once_with(chessMove)


    def test_get_opponent_move(self):
        initial_pos = ChessPosition("b", 4)
        final_pos = ChessPosition("c", 1)
        chessMove = ChessMove(initial_pos, final_pos)

        self.chess_library.getMove = MagicMock(return_value=chessMove)

        opponentMove = self.game_loop.get_opponent_move_from_library()

        self.assertEquals(chessMove, opponentMove)



    @patch("led_interface.LedInterface.turn_on_led")
    def test_show_opponent_move(self, fn):
        initial_pos = ChessPosition("b", 4)
        final_pos = ChessPosition("c", 1)
        chessMove = ChessMove(initial_pos, final_pos)

        self.game_loop.show_opponent_move(initial_pos, final_pos)

        fn.assert_called_with(initial_pos)
        fn.assert_called_with(final_pos)






if __name__ == '__main__':
    unittest.main()