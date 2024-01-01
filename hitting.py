from objects import * 

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

                            # handle doubling: ...if event.unicode == "d" etc 
                            
                            if event.key == pygame.K_RETURN:
                                hand.active = False
                                break

        # while any hands active keep playing
        if any(list(filter(lambda hand : hand.active, game.player.hands))):
            pass
        else:
            # if no hands active but at least one hand not bust
            if any(list(filter(lambda hand : hand.bust, game.player.hands))):
                return False
            else:
                # if all inactive and all bust 
                return True
        
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