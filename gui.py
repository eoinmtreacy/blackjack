import pygame
from pygame.locals import * 
from objects import *

HEIGHT, WIDTH = 480,300

pygame.init()

name_input = Input("red", (HEIGHT-100)/2,(WIDTH-40)/2,100,40)
stack_input = Input("blue", (HEIGHT-100)/2,(WIDTH-40)/2,100,40)

screen = pygame.display.set_mode((HEIGHT,WIDTH))

game_running, setup = True, False
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

    # game loop
    while True:
        screen.fill("grey")

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                    break
        
        for hand in game.player.hands:
            for i, card in enumerate(hand.cards):
                card.rect = pygame.Rect(i * 30, HEIGHT/2, 30, 50)
                card.draw(screen)
        
        for hand in game.dealer.hands:
            for i, card in enumerate(hand.cards):
                card.rect = pygame.Rect(i * 30, 30, 30, 50)
                card.draw(screen)

        pygame.display.update()

pygame.quit()