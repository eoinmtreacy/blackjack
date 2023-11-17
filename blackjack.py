import random
import pygame as pg
from pygame.locals import *

class Card:
    def __init__(self, suit, value):
        self.suits = ("Clubs", "Diamonds", "Hearts", "Spades")
        self.values = (None, "Ace", "2", "3", "4", "5", "6", "7", "8", "9", "Ten", "Jack", "Queen", "King")
        self.suit = self.suits[suit]
        self.value = self.values[value]
    
    def __str__(self):
        return (f"{self.value} of {self.suit}")
        
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
                    newCard = card(s, v)
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
        
    def reset(self, card):
        self.cards = []
        for s in range(4):
            for v in range(13):
                newCard = card(s, v)
                self.cards.append(newCard)
                
    def sort_by_value(self):
        self.cards = sorted(self.cards)

class Hand:
    def __init__(self, card1, card2, wager = 0):
        self.cards = (card1, card2)
        self.wager = wager
        
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
        if self.value() > 21:
            return True
        else:
            return False
        
    def bet(self, wager):
        self.wager = wager

    def __str__(self):
        return (f'{self.cards[0]} {self.cards[1]}')

class Player:
    def __init__(self, name, stack):
        self.name = name
        self.stack = stack
        self.hands = []
    
    def __str__(self):
        return(f'{self.name} has {self.stack} left in their stack')
    
    def add_hand(self,hand):
        self.hands.append(hand)
    
class Game:
    def __init__(self, player, stack, decks):
        self.player = Player(player, stack)
        self.dealer = Player("Dealer", 1000)
        self.deck = Deck(Card, decks)
        self.deck.shuffle()
        
    def hit(self, curr_hand):
        hit = self.deck.draw()
        curr_hand.cards += (hit,)
        print(f'{hit} ({curr_hand.value()})')
        if curr_hand.bust():
            self.player.stack -= 1
            print("Player bust, dealer wins")
            return 1
        else:
            return 0
        
    def deal(self,wager):
        if len(self.deck.cards) != 0:
            print()
            self.player.hands, self.dealer.hands = [Hand(self.deck.draw(), self.deck.draw())], [Hand(self.deck.draw(), self.deck.draw())]
                
            print(f'Dealer showing {self.dealer.hands[0].cards[1]}')
            
            if self.dealer.hands[0].value() == 21 and hand.value() != 21:
                print(f'Dealer has {self.dealer.hands[0].cards[0]}')
                print(f'Dealer wins, blackjack')
                self.player.stack -= wager
                return True
            
            else:
                return False
            
        else:
            print("Deck is empty")

    def read_hand(self, hand):
        print(f"{self.player.name} has", end = " ")
        for card in hand.cards:
            print(card, end = " ")
        print(f'({hand.value()})')
        
        
    def dealerPlay(self):
        print(f'Dealer has', end = ' ')
        for card in self.dealer.hands[0].cards:
            print(card, end=" ")
        print(f'({self.dealer.hands[0].value()})')

        while 17 > self.dealer.hands[0].value():
            hit = self.deck.draw()
            self.dealer.hands[0].cards += (hit,)
            print(f'{hit} ({self.dealer.hands[0].value()})')

        for hand in self.player.hands:
            if self.dealer.hands[0].value() > 21:
                print(f"Dealer busts, you win {hand.wager}")
                self.player.stack += hand.wager
            elif self.dealer.hands[0].value() > hand.value():
                print(f"Dealer wins, you lose {hand.wager}")
                self.player.stack -= hand.wager
            elif self.dealer.hands[0].value() == hand.value():
                print("Push")
            else:
                print(f"You win {hand.wager}")
                self.player.stack += hand.wager

name = input("Enter your name: ")
stack = int(input("Enter your bankroll: "))
decks = int(input("How many decks do you want to play with? "))
newGame = Game(name, stack, decks)

while len(newGame.deck.cards) > decks * 52 /2:
    if newGame.player.stack > 0:
        bet = int(input(f"{newGame.player.stack} remaining, enter bet:"))
        if bet > newGame.player.stack:
            print("Can't bet what you don't have, go home")
            break
        blackjack = newGame.deal(bet)
        if not blackjack:
            for hand in newGame.player.hands:
                hand.wager = bet
                newGame.read_hand(hand)
                while not hand.bust():
                    command = input("H/h to hit, S/s to split, D/d to double, enter to stand: ")
                    if command == "h" or command == "H": 
                        newGame.hit(hand)
                    elif hand.cards[0].value == hand.cards[1].value and command == "s" or command == "S":
                        newGame.player.add_hand(Hand(hand.cards[1], newGame.deck.draw()), bet)
                        hand = Hand(hand.cards[0], newGame.deck.draw(), bet)
                        newGame.read_hand(hand)
                    elif command == "d" or command == "D":
                        hand.wager *= 2
                        newGame.hit(hand)
                        break
                    else:
                        print(f"{newGame.player.name} stands")
                        break
            all_bust = True
            for hand in newGame.player.hands:
                if not hand.bust():
                    all_bust = False
                else:
                    newGame.player.stack -= bet
            if not all_bust:
                newGame.dealerPlay()
    else:
        print("Go home, you're broke")
        break
else:
    print("Halfway through deck, resetting")

print("Finished!")