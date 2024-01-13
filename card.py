import pygame
from pygame.locals import *

class Card:
    def __init__(self, suit, value, img, hidden_img, hidden=False):
        self.hidden = hidden
        self.suits = ("clubs", "diamonds", "hearts", "spades")
        self.colors = ("black", "red", "red", "black")
        self.values = (None, "ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king")
        self.suit = self.suits[suit]
        self.value = self.values[value]
        self.rect = None
        self.color = self.colors[suit]
        self.text = self.value[0] + self.suit[0]
        # self.font = pygame.font.Font('./src/BoecklinsUniverse.tff', 24)
        self.img = img
        self.back = hidden_img
        # print(self.back.get_size())
                                            
    def draw(self, screen, card_w, card_h):
        if not self.hidden:
            screen.blit(pygame.transform.scale(self.img, (card_w, card_h)), self.rect)
            pygame.draw.rect(screen, self.color, self.rect, -1)
            # print(pygame.transform.scale(self.img, (card_w, card_h)).get_size())
        
        else:
            screen.blit(pygame.transform.scale(self.back, (card_w, card_h)), self.rect)
            pygame.draw.rect(screen, self.color, self.rect, -1)
            # print(pygame.transform.scale(self.back, (card_w, card_h)).get_size())

        
    def __str__(self):
        return (f"{self.value} of {self.suit}")