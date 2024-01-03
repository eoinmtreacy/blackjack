import pygame

def draw_cards(game, screen, width, height, menus):
    "handles repetitive drawing of playing pieces"
    
    for i, hand in enumerate(game.player.hands):

            for j, card in enumerate(hand.cards):
                card.rect = pygame.Rect((i * width/len(game.player.hands)) + (j * 30), height/2, 30, 50)
                card.draw(screen)
                hand.draw()

    for menu in menus:
        menu.draw(screen)

    for hand in game.dealer.hands:
        for i, card in enumerate(hand.cards):
            card.rect = pygame.Rect(i * 30, 30, 30, 50)
            card.draw(screen)