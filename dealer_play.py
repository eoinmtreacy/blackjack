from objects import * 

def dealer_play(game, screen, width, height, menus):
    while 17 > game.dealer.hands[0].value:
        print(game.dealer.hands[0].value)
        screen.fill('pink')

        for i, hand in enumerate(game.player.hands):
            for j, card in enumerate(hand.cards):
                card.rect = pygame.Rect((i * width/len(game.player.hands)) + (j * 30), height/2, 30, 50)
                card.draw(screen)

        for menu in menus:
            menu.draw(screen)

        hit = game.deck.draw()
        game.dealer.hands[0].cards += (hit,)
        pygame.time.wait(1000)

        for hand in game.dealer.hands:
            for i, card in enumerate(hand.cards):
                card.rect = pygame.Rect(i * 30, 30, 30, 50)
                card.draw(screen)


        pygame.display.update()

    print("finished!", game.dealer.hands[0].value)