import pygame
from pygame.locals import * 

HEIGHT, WIDTH = 480,300

class Card:
    def __init__(self,color,x,y,h,w):
        self.rect = pygame.Rect(x,y,h,w)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)

class Input:
    def __init__(self,color,x,y,h,w):
        self.rect = pygame.Rect(x,y,h,w)
        self.color = color
        self.text = "something"
        self.font = pygame.font.Font(None, 48)
        self.img = self.font.render(self.text, True, "red")

    def draw(self,screen):
        pygame.draw.rect(screen,self.color, self.rect, 2)

pygame.init()

name_input = Input("red", (HEIGHT-100)/2,( WIDTH-40)/2,100,40)
stack_input = Input("blue", (HEIGHT-100)/2,( WIDTH-40)/2,100,40)

screen = pygame.display.set_mode((HEIGHT,WIDTH))

setup, name, stack = False, False, False
game_running = True
while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    # game set-up: take name and stack size
    if not setup:
        if not name:
            name_input.draw(screen)
        if name and not stack:
            stack_input.draw(screen)
        
    # stack_input.draw(screen)
    
    pygame.display.update()
pygame.quit()