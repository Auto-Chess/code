from chess_move import ChessMove
from chess_position import ChessPosition

import chess.uci

class ChessLibrary():
    def __init__(self):
        # Setup Stockfish engine
        self.engine = chess.uci.popen_engine("stockfish_8_x32")
        self.engine.uci()

    # Give a ChessMove object to the third-party library, push it to board if ok
    def hand_off(self,move):
        if isinstance(move, ChessMove):
            try:
                self.board.push_uci(move.__str__())
                self.engine.position(board)
            except ValueError:
                print("Invalid move: {}!".format(str(move)))
        else:
            raise TypeError("Parameter of hand_off must be of type ChessMove")


    # Asks Chess Library for a move, pushes it to board, and returns it as a ChessMove object
    def get_move(self):
        command = self.engine.go(movetime=2000, async_callback=True)
        best_move, ponder = command.result()
        bm = str(best_move)

        # Converts UCI protocol to ChessPosition via splicing
        init = ChessPosition(str(bm[:1]), int(bm[1:-2]))
        final = ChessPosition(str(bm[2:-1]), int(bm[3:]))


    # Self explanatory
    def is_game_over(self):
        return self.board.is_game_over()
