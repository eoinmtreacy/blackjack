import pygame

class Label:
    "found as a Hand attribute for individual wagers or Game attribute for stack balance"
    def __init__(self, value, x=0, y=0, w=0, h=0, color='white'):
        self.value = "$" + value
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.font = pygame.font.Font("font.ttf", int(h * 0.8))
        self.img = self.font.render(self.value, True, self.color)

    def draw(self, screen):
        center_x, center_y = self.rect.center # find center of input rect
        img_x, img_y = self.img.get_size()
        screen.blit(self.img, (center_x - img_x/2, center_y - img_y/2.3)) # center typed input by taking half the size away from the center
        pygame.draw.rect(screen, self.color, self.rect, -1)

    def update(self, value, color="white"):
        self.value, self.color = value, color
        self.img = self.font.render(self.value, True, self.color)