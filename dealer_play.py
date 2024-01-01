from objects import * 

def dealer_play(game, screen, width, height, menus):
    while True:
        screen.fill('pink')
        print(game.dealer.hands[0].value)

        for i, hand in enumerate(game.player.hands):
            for j, card in enumerate(hand.cards):
                card.rect = pygame.Rect((i * width/len(game.player.hands)) + (j * 30), height/2, 30, 50)
                card.draw(screen)

        for menu in menus:
            menu.draw(screen)

        for hand in game.dealer.hands:
            for i, card in enumerate(hand.cards):
                card.rect = pygame.Rect(i * 30, 30, 30, 50)
                card.draw(screen)

        pygame.display.update()
        pygame.time.wait(1000)
        
        if game.dealer.hands[0].value < 17:
            hit = game.deck.draw()
            game.dealer.hands[0].cards += (hit,)
        else:
            break

    print("finished!", game.dealer.hands[0].value)