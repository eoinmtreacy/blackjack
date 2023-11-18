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
        self.text = ""
        self.font = pygame.font.Font(None, 24)
        self.img = self.font.render(self.text, True, self.color)
        self.active = False

    def draw(self,screen):
        screen.blit(self.img, self.rect)
        pygame.draw.rect(screen,self.color, self.rect, 2)

    def handle_type(self,event):
        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.active = False
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.img = self.font.render(self.text, True, self.color)

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

pygame.quit()