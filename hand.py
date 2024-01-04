from label import Label

class Hand:
    def __init__(self, card1, card2, wager = 0, active = True):
        self.cards = (card1, card2)
        self.wager = wager
        self.active = active
        self.label = Label(str(self.wager), self.cards[0].rect.x, self.cards[0].rect.y - 30, 30, 30, 24)
        
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
    
    def bust(self):
        if self.value > 21:
            self.active = False
            return True
        else:
            return False
        
    def bet(self, wager):
        self.wager = wager

    def __repr__(self):
        return (f'{self.cards[0]} {self.cards[1]}')