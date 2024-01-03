import pygame

from player import Player
from deck import Deck
from hand import Hand
from card import Card
from input import Input

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
        
    def split(self, banker, screen):
        curr_hand = int
        for hand in self.player.hands:
            if hand.active:
                curr_hand = self.player.hands.index(hand)
                break

        wager = self.player.hands[curr_hand].wager

        # create new player hand with second card from splitting hand
        self.player.add_hand(Hand(self.player.hands[curr_hand].cards[1], self.deck.draw(), screen, wager))

        # knock off new hands wager
        banker.account(-wager)

        # replace curr_hand with the hand with same first and new second card 
        self.player.hands[curr_hand] = Hand(self.player.hands[curr_hand].cards[0], self.deck.draw(), screen, wager)
        
    def deal(self, wager, banker, screen):
        if len(self.deck.cards) != 0:
            self.player.hands, self.dealer.hands = [Hand(self.deck.draw(), self.deck.draw(), screen, wager)], [Hand(self.deck.draw(), self.deck.draw(), screen)]
            print(self.player.hands[0].cards[0].y, self.player.hands[0].cards[0].x)
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

    def take_input(color, screen, x, y, w, h):

        new_input = Input(color, x, y, w, h)

        while True:
            screen.fill("grey")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                elif event.type == pygame.KEYDOWN:
                    output = new_input.handle_type(event)
                    if event.key == pygame.K_RETURN:
                        return output

            new_input.draw(screen)
            
            pygame.display.update()
