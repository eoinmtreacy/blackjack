from label import *

class Banker(Label):
    def __init__(self, value, x, y, w, h):
        super().__init__(value, x, y, w, h)

    def account(self, amount):
        self.value = str(int(self.value) + amount)
        self.img = self.font.render(self.value, True, self.color)

class Button:
    def __init__(self, name, x, y, w, h, color, on_click):
        self.name = name
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.font = pygame.font.Font(None, 24)
        self.img = self.font.render(self.name, True, self.color)
        self.on_click = on_click
    
    def draw(self, screen):
        screen.blit(self.img, self.rect)
        pygame.draw.rect(screen, self.color, self.rect, 2)
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
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                pygame.time.wait(250)
                self.handle_click()