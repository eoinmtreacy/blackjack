from objects import * 
from draw_cards import * 

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
            if any(list(filter(lambda hand : hand.bust(), game.player.hands))):
                print("False")
                return False
            else:
                # if all inactive and all bust 
                print("True")
                return True
        
        draw_cards(game, screen, width, height, menus)

        pygame.display.update()