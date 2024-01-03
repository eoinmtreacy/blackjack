from draw_cards import * 

def dealer_play(game, screen, width, height, menus, banker):
    while True:
        screen.fill('pink')
        print(game.dealer.hands[0].value)

        draw_cards(game, screen, width, height, menus)

        pygame.display.update()
        pygame.time.wait(1000)
        
        if game.dealer.hands[0].value < 17:
            hit = game.deck.draw()
            game.dealer.hands[0].cards += (hit,)
        else:
            break

    print("finished!", game.dealer.hands[0].value)