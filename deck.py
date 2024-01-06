from random import shuffle

class Deck:
    def __init__(self, card, number):
        self.cards = []
        for num in range(number):
            for s in range(4):
                for v in range(1,14):
                    newCard = card(s, v, 0, 0)
                    self.cards.append(newCard)
        shuffle(self.cards)
        
    def draw(self):
        return self.cards.pop()