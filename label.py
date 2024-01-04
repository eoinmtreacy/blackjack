import pygame

class Label:
    def __init__(self, value, x, y, w, h, font_size=24):
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