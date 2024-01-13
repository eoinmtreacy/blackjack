import pygame

class Label:
    def __init__(self, value, x=0, y=0, w=0, h=0, font_size=24, color='lightgrey'):
        self.value = value
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.font = pygame.font.Font(None, font_size)
        self.img = self.font.render(self.value, True, self.color)

    def draw(self, screen):
        x, y = self.rect.center # find center of input rect
        screen.blit(self.img, (x - self.img.get_size()[0]/2, y)) # center typed input by taking half the size away from the center
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def update(self, new):
        self.value = new
        self.img = self.font.render(self.value, True, self.color)