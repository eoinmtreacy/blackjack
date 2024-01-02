import pygame
import random
import time
from pygame.locals import *
        
class Input:
    def __init__(self,color,x,y,h,w):
        self.rect = pygame.Rect(x,y,h,w)
        self.color = color
        self.text = ""
        self.font = pygame.font.Font(None, 24)
        self.img = self.font.render(self.text, True, self.color)
        self.active = True

    def draw(self, screen):
        screen.blit(self.img, self.rect.center)
        pygame.draw.rect(screen,self.color, self.rect, 2)

    def handle_type(self,event):
        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.img = self.font.render(self.text, True, self.color)

class Label:
    def __init__(self, value, x, y, w, h):
        self.value = value
        self.rect = pygame.Rect(x, y, w, h)
        self.color = "grey"
        self.font = pygame.font.Font(None, 24)
        self.img = self.font.render(self.value, True, self.color)

    def draw(self, screen):
        screen.blit(self.img, self.rect.center)
        pygame.draw.rect(screen, self.color, self.rect, 2)

class Banker(Label):
    def __init__(self, value, x, y, w, h):
        super().__init__(value, x, y, w, h)

    def account(self, amount):
        self.value = str(int(self.value) + amount)
        self.img = self.font.render(self.value, True, self.color)

class Button:
    def __init__(self, name, x, y, w, h, color, on_click):
        self.name = name
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.font = pygame.font.Font(None, 24)
        self.img = self.font.render(self.name, True, self.color)
        self.on_click = on_click
    
    def draw(self, screen):
        screen.blit(self.img, self.rect)
        pygame.draw.rect(screen, self.color, self.rect, 2)
        self.process()

    def handle_click(self):
        "posts different event to event queue depending on button"

        if self.on_click != " ":
            newevent = pygame.event.Event(pygame.locals.KEYDOWN, unicode=self.on_click, key=pygame.locals.K_a, mod=pygame.locals.KMOD_NONE)
        else:
            newevent = pygame.event.Event(pygame.locals.KEYDOWN, unicode=self.on_click, key=pygame.locals.K_RETURN, mod=pygame.locals.KMOD_NONE)
        pygame.event.post(newevent)

    def process(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                time.sleep(0.25)
                self.handle_click()                

class Card:
    def __init__(self, suit, value, x, y, w=30, h=50):
        self.suits = ("Clubs", "Diamonds", "Hearts", "Spades")
        self.colors = ("black", "red", "red", "black")
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
        
    def __str__(self):
        return (f"{self.value} of {self.suit}")
        
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

class Player:
    def __init__(self, name):
        self.name = name
        self.hands = []
    
    def add_hand(self,hand):
        self.hands.append(hand)

class Hand:
    def __init__(self, card1, card2, wager = 0, active = True):
        self.cards = (card1, card2)
        self.wager = wager
        self.active = active
        
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

    def __str__(self):
        return (f'{self.cards[0]} {self.cards[1]}')
    
class Game:
    def __init__(self, player, decks):
        self.player = Player(player)
        self.dealer = Player("Dealer")
        self.deck = Deck(Card, decks)
        self.deck.shuffle()
        
    def hit(self, curr_hand):
        hit = self.deck.draw()
        curr_hand.cards += (hit,)
        print(f'{hit} ({curr_hand.value})')
        if curr_hand.bust():
            # Banker accounting
            print("Player bust, dealer wins")
            return 1
        else:
            return 0
        
    def split(self, banker):
        curr_hand = int
        for hand in self.player.hands:
            if hand.active:
                curr_hand = self.player.hands.index(hand)
                break

        wager = self.player.hands[curr_hand].wager

        # create new player hand with second card from splitting hand
        self.player.add_hand(Hand(self.player.hands[curr_hand].cards[1], self.deck.draw(), wager))

        # knock off new hands wager
        banker.account(-wager)

        # replace curr_hand with the hand with same first and new second card 
        self.player.hands[curr_hand] = Hand(self.player.hands[curr_hand].cards[0], self.deck.draw(), wager)
        
    def deal(self, wager, banker): # re-add wager
        if len(self.deck.cards) != 0:
            self.player.hands, self.dealer.hands = [Hand(self.deck.draw(), self.deck.draw(), wager)], [Hand(self.deck.draw(), self.deck.draw())]
            
            banker.account(-wager)
            
            if self.dealer.hands[0].value == 21 and self.player.hands[0].value != 21:
                print(f'Dealer wins, blackjack')

                return False
            
            else:
                return True
            
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