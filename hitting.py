from objects import * 
import time

def hitting(game, screen, width, height, menus):
    while True:
        screen.fill("darkgreen")
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                    break
                for hand in game.player.hands:
                    if hand.active: 
                        if event.type == pygame.KEYDOWN:
                            if event.unicode == "h" or event.unicode == "H":
                                game.hit(hand)
                                break
                            if event.unicode == "s" or event.unicode == "S":
                                game.split()
                                break
                            if event.key == pygame.K_RETURN:
                                hand.active = False
                                break

        # hand player bust state, will determine if dealer plays
        done = True
        for hand in game.player.hands:
            if hand.active:
                done = False
                pygame.time.delay(100)
            if hand.bust:
                bust = True
        if done:
            print(bust, "hitting.py")
            return bust
        
        for i, hand in enumerate(game.player.hands):
            for j, card in enumerate(hand.cards):
                card.rect = pygame.Rect((i * width/len(game.player.hands)) + (j * 30), height/2, 30, 50)
                card.draw(screen)
        
        for hand in game.dealer.hands:
            for i, card in enumerate(hand.cards):
                card.rect = pygame.Rect(i * 30, 30, 30, 50)
                card.draw(screen)

        for menu in menus:
            menu.draw(screen)

        pygame.display.update()