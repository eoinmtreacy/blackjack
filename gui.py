import pygame
from pygame.locals import * 
from objects import *

WIDTH, HEIGHT = 480, 300

pygame.init()

name_input = Input("red", (WIDTH-100)/2,(HEIGHT-40)/2,100,40)
stack_input = Input("blue", (WIDTH-100)/2,(HEIGHT-40)/2,100,40)

screen = pygame.display.set_mode((WIDTH,HEIGHT))

game_running = True
name_input.active = True

while game_running:
    
    # game set-up:
    while name_input.active or stack_input.active:
        
        # enter name
        while name_input.active:
            screen.fill("grey")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                NAME = name_input.handle_type(event)

            if name_input.active:
                name_input.draw(screen)
            
            pygame.display.update()
        
        stack_input.active = True
        
        # enter stack
        while stack_input.active:
            screen.fill("grey")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                STACK = stack_input.handle_type(event)

            if stack_input.active:
                stack_input.draw(screen)
            
            pygame.display.update()

    
    # game object takes player name, stack and no. of decks
    game = Game(NAME, int(STACK), 1)
    game.deal()
    name_label = Label(NAME, 20, (HEIGHT/4) * 3 , WIDTH/7, HEIGHT/8)
    stack_label = Label(str(game.player.stack), 120, (HEIGHT/4) * 3, WIDTH/7, HEIGHT/8, STACK)
    hit_button = Button("hit", WIDTH/2, HEIGHT/4 * 3, 30, 30, "red")
    split_button = Button("split", WIDTH/2 + 30, HEIGHT/4 * 3, 60, 30, "yellow")
    stand_button = Button("stand", WIDTH/2 + 90, HEIGHT/4 * 3, 60, 30, "grey")
    double_button = Button("double", WIDTH/2 + 150, HEIGHT/4 * 3, 60, 30, "hotpink")
    # hit = Button
    # game loop
    while True:
        split = False
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
                                split = True
                                break
                            if event.key == pygame.K_RETURN:
                                hand.active = False
                                break

        if split:
            game.split()
            split = False

        for i, hand in enumerate(game.player.hands):
            for j, card in enumerate(hand.cards):
                card.rect = pygame.Rect((i * WIDTH/len(game.player.hands)) + (j * 30), HEIGHT/2, 30, 50)
                card.draw(screen)
        
        for hand in game.dealer.hands:
            for i, card in enumerate(hand.cards):
                card.rect = pygame.Rect(i * 30, 30, 30, 50)
                card.draw(screen)

        for label in [name_label, stack_label]:
            label.draw(screen)

        for button in [hit_button, stand_button, split_button, double_button]:
            button.draw(screen)

        pygame.display.update()

pygame.quit()