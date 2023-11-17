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
        self.active = False

    def draw(self,screen):
        pygame.draw.rect(screen,self.color, self.rect, 2)

    def handle_type(self,event):
        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.text = ''
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.img = self.font.render(self.text, True, "red")

pygame.init()

name_input = Input("red", (HEIGHT-100)/2,( WIDTH-40)/2,100,40)
stack_input = Input("blue", (HEIGHT-100)/2,( WIDTH-40)/2,100,40)

screen = pygame.display.set_mode((HEIGHT,WIDTH))

setup, name_input.active, stack_input.active = False, True, False
game_running = True
while game_running:
    

    # game set-up: take name and stack size
    if not setup:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            for input in [name_input, stack_input]:
                input.handle_type(event)
        if name_input.active:
            name_input.draw(screen)
        if not name_input.active:
            stack_input.active = True
            stack_input.draw(screen)
    
    pygame.display.update()
pygame.quit()