from chess_move import ChessMove
from chess_position import ChessPosition

import chess.uci


class ChessLibrary():
    def __init__(self):
        # Setup Stockfish engine
        self.board = chess.Board()
        self.engine = chess.uci.popen_engine("stockfish_8")
        self.engine.uci()


    # Give a ChessMove object to the third-party library, push it to board if ok
    def hand_off(self, move):
        if isinstance(move, ChessMove):
            try:
                self.board.push_uci(str(move))
                self.engine.position(self.board)

            except ValueError as e:
                raise ValueError("Invalid move: {}".format(str(move)))
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

        move = ChessMove(init, final)

        self.board.push_uci(str(move))
        return move


    # Self explanatory
    def is_game_over(self):
        return self.board.is_game_over()
      
    # Sets difficulty. Must be between 0 and 20, 20 being hardest
    def set_difficulty(self, difficulty):
        if difficulty < 0 or difficulty > 20:
            raise ValueError("Difficulty must be between 0 and 20")
        else:
            new_options = {'Skill Level': difficulty}
            self.engine.setoption(new_options)

    # Gets difficulty
    def get_difficulty(self):
        return 0