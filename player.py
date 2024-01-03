class Player:
    def __init__(self, name):
        self.name = name
        self.hands = []
    
    def add_hand(self,hand):
        self.hands.append(hand)