import pygame

class Label:
    def __init__(self, value, x=0, y=0, w=0, h=0, font_size=24):
        self.value = value
        self.rect = pygame.Rect(x, y, w, h)
        self.color = "lightgrey"
        self.font = pygame.font.Font(None, font_size)
        self.img = self.font.render(self.value, True, self.color)

    def draw(self, screen):
        screen.blit(self.img, self.rect.center)
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def update(self, new):
        self.value = new