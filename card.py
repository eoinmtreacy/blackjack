import pygame
from pygame.locals import *

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
            # print(pygame.transform.scale(self.img, (card_w, card_h)).get_size())
        
        else:
            screen.blit(pygame.transform.scale(self.back, (card_w, card_h)), self.rect)
            pygame.draw.rect(screen, self.color, self.rect, -1)
            # print(pygame.transform.scale(self.back, (card_w, card_h)).get_size())