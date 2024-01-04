from input import *
from hitting import *
from settle import *
from game import Game

"""
game init

    game.wager()
    game.deal()

    game.hitting()
        game.draw
    game.dealerplay
        game.draw()
    game.settle()
        game.draw()


"""

if __name__ == "__main__" :
    game = Game()
    game.on_execute()