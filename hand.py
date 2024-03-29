from pygame import (Rect, draw)
# from pygame.locals import *
from label import Label

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

