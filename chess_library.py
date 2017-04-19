from chess_move import ChessMove
from chess_position import ChessPosition

def handoff(self, move):
    #Give a ChessMove object to the third-party library
    return 0

def getmove(self):
    #Asking Chess Library for a move, and storing it into a ChessPosition object
    #In this example, the original pos is 0,0 and the final is 1,1
    init = ChessPosition(0, 0)
    final = ChessPosition(1, 1)

    return ChessMove(init, final)


