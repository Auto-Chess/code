from chess_move import ChessMove
from chess_position import ChessPosition

import chess.uci


class ChessLibrary():
    def __init__(self):
        # Setup Stockfish engine
        self.difficulty = 20
        self.board = chess.Board()
        self.engine = chess.uci.popen_engine("stockfish_8")
        self.engine.uci()
        
    """Gives a ChessMove object to the third-party library, which is then pushed to the board if ok
    Arg:
        - move: A ChessMove object which is then translated into a UCI move
    Raises:
        - ValueError: Raised if the move given is illegal
        - TypeError: Raised if parameter 'move' is not of type ChessMove
    """
    def hand_off(self, move):
        if isinstance(move, ChessMove):
            try:
                self.board.push_uci(move.__str__())
                self.engine.position(self.board)
            except ValueError:
                raise ValueError("Invalid move: {}!".format(str(move)))
        else:
            raise TypeError("Parameter of hand_off must be of type ChessMove")

    """Asks Chess Library for a move, pushes it to board, and returns it as a ChessMove object
    Returns:
        - A ChessMove object which shows where the chess engine decided to move
    """
    def get_move(self):
        command = self.engine.go(movetime=2000, async_callback=True)
        print(type(command))
        best_move, ponder = command.result()
        bm = str(best_move)

        # Converts UCI protocol to ChessPosition via slicing
        init = ChessPosition(str(bm[:1]), int(bm[1:-2]))
        final = ChessPosition(str(bm[2:-1]), int(bm[3:]))

        return ChessMove(init, final)

    """Evaluates whether the game is over or not
    Returns:
        - A boolean which is true if the game has ended, false if not
    """
    def is_game_over(self):
        return self.board.is_game_over()
      
    """Sets difficulty. Must be between 0 and 20, 20 being hardest
    Raises:
        - ValueError: Raised if the difficulty is not within legal boundaries 
    """
    def set_difficulty(self, difficulty):
        if difficulty < 0 or difficulty > 20:
            raise ValueError("Difficulty must be between 0 and 20 inclusive")
        else:
            new_options = {'Skill Level': difficulty}
            self.engine.setoption(new_options)
            self.difficulty = difficulty

    # Clears the board and then tells Stockfish a new game has started
    def start_game(self):
        self.board.reset()
        # self.engine.position(self.board)
        self.engine.ucinewgame()

    def get_difficulty(self):
        return self.difficulty


'''
y = ChessLibrary()
a = ChessPosition("e", 2)
b = ChessPosition("e", 4)
x = ChessMove(a, b)
y.hand_off(x)
y.get_move()
'''