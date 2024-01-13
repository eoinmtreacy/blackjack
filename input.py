import pygame

class Input:
    def __init__(self,color,x,y,h,w):
        self.rect = pygame.Rect(x,y,h,w)
        self.color = color
        self.text = ""
        self.font = pygame.font.Font(None, 24)
        self.img = self.font.render(self.text, True, self.color)
        self.active = True

    def draw(self, screen):
        x, y = self.rect.center # find center of input rect
        screen.blit(self.img, (x - self.img.get_size()[0]/2, y)) # center typed input by taking half the size away from the center
        pygame.draw.rect(screen, self.color, self.rect, 2)
        # input(self.img.get_size()[0])
        

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