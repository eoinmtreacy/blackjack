import pygame
import random
from pygame.locals import *
        
class Input:
    def __init__(self,color,x,y,h,w):
        self.rect = pygame.Rect(x,y,h,w)
        self.color = color
        self.text = ""
        self.font = pygame.font.Font(None, 24)
        self.img = self.font.render(self.text, True, self.color)
        self.active = False

    def draw(self,screen):
        screen.blit(self.img, self.rect)
        pygame.draw.rect(screen,self.color, self.rect, 2)

    def handle_type(self,event):
        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.active = False
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.img = self.font.render(self.text, True, self.color)

class Card:
    def __init__(self, suit, value, x, y, w=30, h=50):
        self.suits = ("Clubs", "Diamonds", "Hearts", "Spades")
        self.colors = ("green", "blue", "red", "black")
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
        
class Deck:
    def __init__(self, card, number):
        self.cards = []
        for num in range(number):
            for s in range(4):
                for v in range(1,14):
                    newCard = card(s, v, 0, 0)
                    self.cards.append(newCard)
        
    def draw(self):
        try:
            card = self.cards[-1]
            self.cards.pop()
            return card
        except:
            return False
            
    def shuffle(self):
        random.shuffle(self.cards)