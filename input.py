import pygame

class Input:
    def __init__(self,color,x,y,w, h):
        self.size = self.width, self.height = (w, h)
        self.pos = self.x, self.y = (x, y)
        self.rect = pygame.Rect(self.pos, self.size)
        self.color = color
        self.text = ""
        self.font = pygame.font.Font('font.ttf', int(self.height * 0.7))
        self.img = self.font.render(self.text, True, self.color)
        self.border = pygame.image.load('./src/input.png')
        self.active = True

    def draw(self, screen):
        center_x, center_y = self.rect.center # find center of input rect
        img_x, img_y = self.img.get_size() # find the size of the text
        screen.blit(self.img, (center_x - img_x/2, center_y - img_y/2)) # blit to center
        screen.blit(pygame.transform.scale(self.border, self.size), self.rect) # blit to center
        pygame.draw.rect(screen, self.color, self.rect, -1)

    def handle_type(self,event):
        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.unicode in '0123456789':
                    self.text += event.unicode
                # Re-render the text.
                self.img = self.font.render(self.text, True, self.color)