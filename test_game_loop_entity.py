import unittest
from chess_library import ChessLibrary
from game_loop_entity import GameLoopEntity
from chess_position import ChessPosition
from chess_move import ChessMove
from led_interface import LedInterface
from mock import MagicMock
from mock import patch
from mock import call

class TestGameLoopEntity(unittest.TestCase):
    def setUp(self):
        self.chess_library = ChessLibrary()
        self.game_loop = GameLoopEntity()
        self.led_interface = LedInterface()

    @patch("chess_library.ChessLibrary.hand_off")
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

        self.game_loop.chess_library.get_move = MagicMock(return_value=chessMove)

        opponentMove = self.game_loop.get_opponent_move_from_library()

        self.assertEquals(chessMove, opponentMove)

    @patch("led_interface.LedInterface.start_blinking_led")
    @patch("led_interface.LedInterface.turn_on_led")
    def test_show_opponent_move(self, turn_on_led_checker, start_blinking_led_checker):
        initial_pos = ChessPosition("b", 4)
        final_pos = ChessPosition("c", 1)
        chessMove = ChessMove(initial_pos, final_pos)

        self.game_loop.show_opponent_move(initial_pos, final_pos)

        turn_on_led_checker.assert_called_with(initial_pos)
        start_blinking_led_checker.assert_called_with(final_pos, 1)

    @patch("builtins.input", side_effect = ["b4","c5"])
    def test_gather_user_input(self, input_checker):
        result = self.game_loop.gather_user_input()
        initial_pos = ChessPosition("b", 4)
        final_pos = ChessPosition("c", 5)
        chessMove = ChessMove(initial_pos, final_pos)

        self.assertEquals(result, chessMove)

    @patch("lcd_interface.LCDInterface.display")
    def test_prompt_user_for_beginning_input(self, display_checker):
        self.game_loop.prompt_user_for_input()
        display_checker.assert_has_calls([call("Welcome to Auto Chess", ""), call("Enter initial then final position: ","")])

    @patch("lcd_interface.LCDInterface.display")
    def test_prompt_user_for_other_input(self, display_checker):
        self.game_loop.prompt_user_for_input()
        display_checker.assert_called_with("Enter initial then final position: ", "")

    @patch("builtins.input", side_effect=["z20", "b4", "c5"])
    def test_gather_user_input_initial_check(self, input_checker):
        self.game_loop.lcd_interface.display = MagicMock()
        result = self.game_loop.gather_user_input()

        self.game_loop.lcd_interface.display.assert_called_once_with("Incorrect initial coordinate, try again.", "")

        initial_pos = ChessPosition("b", 4)
        final_pos = ChessPosition("c", 5)
        chessMove = ChessMove(initial_pos, final_pos)

        self.assertEquals(result, chessMove)

    @patch("builtins.input", side_effect=["b4", "z20", "c5"])
    def test_gather_user_input_final_check(self, input_checker):
        self.game_loop.lcd_interface.display = MagicMock()
        result = self.game_loop.gather_user_input()

        self.game_loop.lcd_interface.display.assert_called_once_with("Incorrect final coordinate, try again.", "")

        initial_pos = ChessPosition("b", 4)
        final_pos = ChessPosition("c", 5)
        chessMove = ChessMove(initial_pos, final_pos)

        self.assertEquals(result, chessMove)