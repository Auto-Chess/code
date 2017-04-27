from chess_move import ChessMove
from chess_position import ChessPosition

import chess

# This object is created purely for testing purposes as of now
board = chess.Board()


# Give a ChessMove object to the third-party library
def hand_off(move):
    if isinstance(move, ChessMove):
        board.parse_uci(move.__str__())
    else:
        raise TypeError("Parameter of hand_off must be of type ChessMove")


# Asks Chess Library for a move, and returns it as a ChessMove object
def get_move():
    init = ChessPosition("a", 0)
    final = ChessPosition("a", 0)

    return ChessMove(init, final)