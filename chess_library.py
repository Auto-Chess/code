from code import chess_move
from code import chess_position

class ChessLibrary:

    def handoff(self, move):
        #use whatever method 3rd party library to hand it information from the object "move", which
        #is a ChessMove object
        return 0;

    def getmove(self):
        sentence = 'Asking library for AI move... Done. Returning (x), (y)'
        print(sentence)
        x = 0
        y = 0

        move = ChessMove(x, y)
        return move
