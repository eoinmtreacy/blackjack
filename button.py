import pygame
import time

class Button:
    def __init__(self, name, x, y, w, on_click):
        self.name = name
        self.size = self.width, self.height = w/64*6, w/64*6
        self.rect = pygame.Rect((x, y), (self.size))
        self.font = pygame.font.SysFont('Helvetica', 24)
        self.img = pygame.image.load(f'./src/buttons/{name}.png')
        self.on_click = on_click
    
    def draw(self, screen):
        screen.blit(pygame.transform.scale(self.img, (self.width, self.height)), self.rect)
        pygame.draw.rect(screen, "grey", self.rect, -1)
        self.process()

    def handle_click(self):
        "posts different event to event queue depending on button"

        if self.on_click != " ":
            newevent = pygame.event.Event(pygame.locals.KEYDOWN, unicode=self.on_click, key=pygame.locals.K_a, mod=pygame.locals.KMOD_NONE)
        else:
            newevent = pygame.event.Event(pygame.locals.KEYDOWN, unicode=self.on_click, key=pygame.locals.K_RETURN, mod=pygame.locals.KMOD_NONE)
        pygame.event.post(newevent)

    def process(self):
        pos = pygame.mouse.get_pos()
        print(pos)
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                print("click")
                time.sleep(0.25)
                self.handle_click() 