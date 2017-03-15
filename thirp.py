"""
What's up Youtube, today I'm going to be bringing you a playthrough of 
a third party chess library. Hopefully I can get some good clips for
you guys today.

Okay are you ready? Let's go.
"""

import collections

class Chessbrary():
    
    def handOff(self, moveX, moveY):
        #TODO: figure out how to "give" the library a move. Where does the library exist?
        #How does Chessbrary have access to it?
    
        sentence = 'Giving {} and {} to chess library.'.format(moveX, moveY)
        print(sentence)
        
    def getMove(self):
        #TODO: figure out how the library will be "asked" for a move. By what means does
        #it take input? Doesn't having this class kind of negate the purpose of the other
        #method I wrote? Should exception handling be done within here?
    
        sentence = 'Asking library for AI move... Done. Returning (x), (y)'
        print(sentence)
        x = 0
        y = 0
        return x, y
        
    #def getStatus():
        #hypothetical function that returns the state of the game, for example: Player won,
        #Player lost, Player's turn, Opponent's turn, etc. Could be used within game loop?
        
#x = Chessbrary()
#x.handOff(3, 4)
#x.getMove()

"""
Thanks for watching, and remember to like, comment, and subscribe.
"""