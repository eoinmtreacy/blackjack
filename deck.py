from random import shuffle
import pygame 

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