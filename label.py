import pygame

class Label:
    def __init__(self, value, x=0, y=0, w=0, h=0, font_size=24, color='lightgrey'):
        self.value = value + "$"
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.font = pygame.font.Font("font.ttf", 65)
        self.img = self.font.render(self.value, True, self.color)

    def draw(self, screen):
        center_x, center_y = self.rect.center # find center of input rect
        img_x, img_y = self.img.get_size()
        screen.blit(self.img, (center_x - img_x/2, center_y - img_y/2)) # center typed input by taking half the size away from the center
        pygame.draw.rect(screen, self.color, self.rect, -1)

    def update(self, new):
        self.value = new
        self.img = self.font.render(self.value, True, self.color)