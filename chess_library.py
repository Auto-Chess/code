from chess_move import ChessMove
from chess_position import ChessPosition

import chess.uci

# This object is created purely for testing purposes as of now, but might exist permanently in this class later
board = chess.Board()

# Setup Stockfish engine
engine = chess.uci.popen_engine("/stockfish_8_x32")
engine.uci()


# Give a ChessMove object to the third-party library, push it to board if ok
def hand_off(move):
    if isinstance(move, ChessMove):
        try:
            board.push_uci(move.__str__())
            engine.position(board)
        except ValueError:
            print('\033[91m' + "Invalid move: " + move.__str__() + "!" + '\033[0m')
            return False
    elif isinstance(move, str):
        try:
            board.push_uci(move)
            engine.position(board)
        except ValueError:
            print('\033[91m' + "Invalid move: " + move + "!" + '\033[0m')
            return False
    else:
        raise TypeError("Parameter of hand_off must be of type ChessMove or String")
    return True


# Asks Chess Library for a move, pushes it to board, and returns it as a ChessMove object
def get_move():
    command = engine.go(movetime=2000, async_callback=True)
    best_move, ponder = command.result()
    bm = str(best_move)

    # Converts UCI protocol to ChessPosition via splicing
    init = ChessPosition(str(bm[:1]), int(bm[1:-2]))
    final = ChessPosition(str(bm[2:-1]), int(bm[3:]))

    board.push_uci(str(best_move))
    engine.position(board)

    return ChessMove(init, final)


# Self explanatory
def is_game_over():
    return board.is_game_over();


# Test code. Very rough but it works
while not is_game_over():
    x = get_move()
    print(x.__str__())
    y = False
    while not y:
        y = hand_off(input("Enter move: "))
