import collections


class ChessLibrary():
    def handOff(self, moveX, moveY):

        sentence = 'Giving {} and {} to chess library.'.format(moveX, moveY)
        print(sentence)

    def getMove(self):

        sentence = 'Asking library for AI move... Done. Returning (x), (y)'
        print(sentence)
        x = 0
        y = 0
        return x, y
