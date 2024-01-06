from pygame import (Rect, draw)
from pygame.locals import *
from label import Label

class Hand:
    def __init__(self, card1, card2, wager = 0, active = True):
        self.cards = (card1, card2)
        self.wager = wager
        self.active = active
        self.rect = None
        self.color = 'yellow'

    def __repr__(self):
        return (f'{self.cards[0]} {self.cards[1]}')
    
    def draw(self, screen, card_w, card_h):
        # screen.blit(self.img, self.rect.center) -- may need to blit later but okay for now
        draw.rect(screen, self.color, self.rect, 2)
        for c, card in enumerate(self.cards):
            card.rect = Rect(self.rect.x + c * card_w, self.rect.y, card_w, card_h)
            card.draw(screen)

    @property
    def value(self):
        value = 0
        for card in self.cards:
            addition = 10 if card.values.index(card.value) > 10 else card.values.index(card.value)
            value += addition
            if value + 10 < 22:
                if card.value == "Ace":
                    value += 10
        return value
    
    @property
    def bust(self):
        if self.value > 21:
            self.active = False
            return True
        else:
            return False

