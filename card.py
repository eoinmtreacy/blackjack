import pygame
from pygame.locals import *

class Card:
    def __init__(self, suit, value, hidden=False):
        self.hidden = hidden
        self.suits = ("clubs", "diamonds", "hearts", "spades")
        self.colors = ("black", "red", "red", "black")
        self.values = (None, "Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king")
        self.suit = self.suits[suit]
        self.value = self.values[value]
        self.rect = None
        self.color = self.colors[suit]
        self.text = self.value[0] + self.suit[0]
        self.font = pygame.font.SysFont('Helvetica', 24)
        self.img = self.font.render(self.text, True, self.color)
        # self.img = pygame.image.load(f'./src/English_pattern_{self.value}_of_{self.suit}.svg')


    def draw(self,screen, card_w, card_h):
        if not self.hidden:
            screen.blit(pygame.transform.scale(self.img, (card_w, card_h)), self.rect)
            pygame.draw.rect(screen, self.color, self.rect, 2)
        
    def __str__(self):
        return (f"{self.value} of {self.suit}")