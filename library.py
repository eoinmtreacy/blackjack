import pygame
from pygame.locals import *
import time
from random import shuffle

class Input:
    def __init__(self, x, y, w, h):
        self.size = self.width, self.height = (w, h)
        self.pos = self.x, self.y = (x, y)
        self.rect = pygame.Rect(self.pos, self.size)
        self.text = ""
        self.font = pygame.font.Font('font.ttf', int(self.height * 0.7))
        self.img = self.font.render(self.text, True, "white")
        self.border = pygame.image.load('./src/input.png')
        self.active = True

    def draw(self, screen):
        center_x, center_y = self.rect.center # find center of input rect
        img_x, img_y = self.img.get_size() # find the size of the text
        screen.blit(self.img, (center_x - img_x/2, center_y - img_y/2)) # blit to center
        screen.blit(pygame.transform.scale(self.border, self.size), self.rect) # blit to center
        pygame.draw.rect(screen, "white", self.rect, -1)

    def handle_type(self, event):
        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.unicode in '0123456789':
                    self.text += event.unicode
                # Re-render the text.
                self.img = self.font.render(self.text, True, "white")

class Button:
    def __init__(self, name, x, y, w, on_click):
        self.name = name
        self.size = self.width, self.height = w/64*6, w/64*6
        self.rect = pygame.Rect((x, y), (self.size))
        # self.font = pygame.font.SysFont('Helvetica', 24)
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
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                time.sleep(0.25)
                self.handle_click() 

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

class Card:
    def __init__(self, suit, value, img, back, hidden=False):
        self.hidden = hidden
        self.suits = ("clubs", "diamonds", "hearts", "spades")
        self.values = (None, "ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king")
        self.suit = self.suits[suit]
        self.value = self.values[value]
        self.rect = None # rect handled by game.draw()
        self.color = "white"
        self.img = img
        self.back = back
                                            
    def draw(self, screen, card_w, card_h):
        if not self.hidden:
            screen.blit(pygame.transform.scale(self.img, (card_w, card_h)), self.rect)
            pygame.draw.rect(screen, self.color, self.rect, -1)
        
        else:
            screen.blit(pygame.transform.scale(self.back, (card_w, card_h)), self.rect)
            pygame.draw.rect(screen, self.color, self.rect, -1)

class Deck:
    "container for cards, used in init to load card face and back images"
    def __init__(self, card, number):
        self.values = [None, "ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"]
        self.suits = ["clubs", "diamonds", "hearts", "spades"]
        self.hidden_img = pygame.image.load('./src/cards/hidden.svg')
        self.images = {}

        for value in self.values:
            for suit in self.suits:
                try:
                    self.images[f'{value}{suit}'] = pygame.image.load(f'./src/cards/English_pattern_{value}_of_{suit}.svg')
                except:
                    pass

        self.cards = []

        for _ in range(number):
            for s in range(4):
                for v in range(1,14):
                    newCard = card(s, v, self.images[f'{self.values[v]}{self.suits[s]}'], self.hidden_img)
                    self.cards.append(newCard)
        shuffle(self.cards)
        
    def draw(self, hidden=False):
        card = self.cards.pop()
        card.hidden = hidden
        return card

class Player:
    def __init__(self, name):
        self.name = name
        self.hands = []

class Hand:
    def __init__(self, card1, card2, label_size, wager = 0, active = True):
        self.cards = (card1, card2)
        self.wager = wager
        self.active = active
        self.label = Label(str(self.wager), w=label_size, h=label_size)
    
    def draw(self, screen, card_w, card_h):
        if self.wager: # stops wager label drawing on dealer cards
            self.label.rect = Rect(self.rect.x, self.rect.y - card_w, card_w, card_w) # wager label, reference rect via game.draw()
            self.label.draw(screen)
        for c, card in enumerate(self.cards):
            card.rect = Rect(self.rect.x + c * card_w, self.rect.y, card_w, card_h)
            card.draw(screen, card_w, card_h)

    @property
    def value(self):
        value = 0
        for card in self.cards:
            add = 10 if card.values.index(card.value) > 10 else card.values.index(card.value)
            value += add

        if value + 10 < 22:
            aces = [card.value for card in self.cards].count("ace")
            for ace in range(aces):
                value += 10
                if value + 10 > 21:
                    break
            
        return value
    
    @property
    def bust(self):
        if self.value > 21:
            self.active = False
            self.label = Label("0", color='crimson')
            return True
        else:
            return False