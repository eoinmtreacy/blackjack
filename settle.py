import pygame
from draw_cards import *

def settle(game, screen, w, h, menus, banker):
    "handles wager and banker methods for each hand in player hands"

    for hand in game.player.hands:
        pygame.time.wait(1000) # so player can see what's going on
        screen.fill("aqua")
        draw_cards(game, screen, w, h, menus)

        if hand.bust():
            print(f'Hand busted, you lose {hand.wager}')

        elif game.dealer.hands[0].bust():
            print(f'Dealer bust, hand wins {hand.wager}')

            banker.account(hand.wager * 2)
        elif game.dealer.hands[0].value > hand.value:
            print(f'Dealer wins, you lose {hand.wager}')

        elif hand.value > game.dealer.hands[0].value:
            print(f'Hand holds, you win {hand.wager}')
            banker.account(hand.wager * 2)

        else:
            print('Push')
            banker.account(hand.wager)