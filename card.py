import pygame
from pygame.locals import *

class Card:
    def __init__(self, suit, value, x, y, w=30, h=50):
        self.x = x
        self.y = y
        self.suits = ("Clubs", "Diamonds", "Hearts", "Spades")
        self.colors = ("black", "red", "red", "black")
        self.values = (None, "Ace", "2", "3", "4", "5", "6", "7", "8", "9", "Ten", "Jack", "Queen", "King")
        self.suit = self.suits[suit]
        self.value = self.values[value]
        self.rect = pygame.Rect(x,y,w,h)
        self.color = self.colors[suit]
        self.text = self.value[0] + self.suit[0]
        self.font = pygame.font.Font(None, 24)
        self.img = self.font.render(self.text, True, self.color)

    def draw(self,screen):
        screen.blit(self.img, self.rect)
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def __eq__(self, other):
        return self.value == other.value
    
    def __gt__(self, other):
        if self.values.index(self.value) > other.values.index(other.value):
            return True
        elif self.suits.index(self.suit) > other.suits.index(other.suit) and self.values.index(self.value) == other.values.index(other.value):
            return True
        else:
            return False
        
    def __str__(self):
        return (f"{self.value} of {self.suit}")