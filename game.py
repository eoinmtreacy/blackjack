import pygame
from pygame.locals import * 

from player import Player
from deck import Deck
from hand import Hand
from card import Card
from input import Input
from button import Button
from label import Label

class Game:
    def __init__(self):
        pygame.init()
        self.size = self.width, self.height = 480, 300
        self.card_w, self.card_h = self.width/16, self.height/6
        self._screen = pygame.display.set_mode((self.size))
        self._running = True
        self.player = Player("Player")
        self.stack = 1000 #stack tied to game, not player, up for debate, not sure if more than one player in needed
        self.dealer = Player("Dealer")
        self.deck = Deck(Card,8)
        self.buttons = {
            'hit': Button("hit", self.width/2, self.height/4 * 3, 30, 30, "red", "h"),
            'split': Button("split", self.width/2 + 30, self.height/4 * 3, 60, 30, "yellow", "s"),
            'stand': Button("stand", self.width/2 + 90, self.height/4 * 3, 60, 30, "grey", " "),
            'double': Button("double", self.width/2 + 150, self.height/4 * 3, 60, 30, "hotpink", "d")
        }
        self.labels = {
            'stack': Label(str(self.stack), self.width/6, (self.height/4) * 3, self.width/7, self.height/8)
        }
    
    def on_execute(self):
        while(self._running):
            for event in pygame.event.get():
                self.on_event(event)
            wager = self.get_wager()
            blackjack = self.deal(wager)
            if not blackjack:
                bust = self.hitting(wager)
                self.dealer.hands[0].cards[0].hidden = False # unhide dealer hole card at end of hitting
                if not bust:
                    self.dealer_play()
            self.dealer.hands[0].cards[0].hidden = False # unhide dealer hole card if blackjack
            self.settle()
        self.on_cleanup()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def get_wager(self):
        new_input = Input('green', self.width/8*3, self.height/8*3, self.width/4, self.height/8)
        self.draw()
        new_input.draw(self._screen)
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                elif event.type == pygame.KEYDOWN:
                    output = new_input.handle_type(event)
                    if event.key == pygame.K_RETURN and output != '':
                        return int(output)
                    self.draw()
                    new_input.draw(self._screen)
                    pygame.display.update()
            

    def deal(self, wager):
        "first subloop add cards to hands and hands to player and dealer"

        if len(self.deck.cards) != 0:
            self.player.hands, self.dealer.hands = [Hand(self.deck.draw(), self.deck.draw(), wager)], [Hand(self.deck.draw(True), self.deck.draw())]
            self.account(-wager)
            self.draw()
            
            if self.dealer.hands[0].value == 21 and self.player.hands[0].value != 21:
                print(f'Blackjack, dealer wins')
                return True
            elif self.dealer.hands[0].value != 21 and self.player.hands[0].value == 21:
                print(f'Player blackjack, you lucky duck')
                return True
            elif self.dealer.hands[0].value == 21 and self.player.hands[0].value == 21:
                print(f'Both dealt blackjack (...what are the odds... about 0.22% at an even cout)')
                return True
            else:
                return False
        else:
            print("Deck is empty")

    def hitting(self, wager):
        "if not dealer blackjack (peak), await user input"

        while True:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                    break
                for hand in self.player.hands:
                    if hand.active: 
                        if event.type == pygame.KEYDOWN:

                            if event.unicode == "h" or event.unicode == "H":
                                self.hit(hand)
                                break

                            if (event.unicode == "s" or event.unicode == "S"): #and len(hand.cards) == 2 and hand.cards[0].value == hand.cards[1].value:
                                if wager <= self.stack:
                                    self.split(wager)
                                    break
                                else:
                                    print("You don't have enough to split")
                            
                            if (event.unicode == "d" or event.unicode == "D"):
                                if wager <= self.stack:
                                    hand.wager *= 2
                                    hand.label.update(str(wager * 2))
                                    hand.active = False
                                    self.account(-wager)
                                    self.hit(hand)
                                    break
                                else:
                                    print("You don't have enough to double")

                            if event.key == pygame.K_RETURN:
                                hand.active = False
                                break

            # while any hands active keep playing
            if any([hand.active for hand in self.player.hands]):
                pass
            else:
                # all hands.bust == true
                if all([hand.bust for hand in self.player.hands]):
                    print("True")
                    return True
                else:
                    # at least one not bust 
                    print("False")
                    return False

    def dealer_play(self):
        "dealer stands on 17 otherwise hits"

        while True:
            self.draw()
            pygame.time.wait(1000)

            if self.dealer.hands[0].value < 17:
                hit = self.deck.draw()
                self.dealer.hands[0].cards += (hit,)
            else:
                break
        
    def settle(self):
        "for each player hands settles up with dealer"

        for hand in self.player.hands:
            self.draw()
            pygame.time.wait(1000)

            if hand.bust:
                print(f'Hand busted, you lose {hand.wager}')

            elif self.dealer.hands[0].bust:
                print(f'Dealer bust, hand wins {hand.wager}')
                self.account(hand.wager * 2)

            elif hand.value == 21 and len(hand.cards) == 2 and self.dealer.hands[0].value != 21:
                print(f'Blackjack plays 2:1, you win {hand.wager * 3}')

            elif self.dealer.hands[0].value > hand.value:
                print(f'Dealer wins, you lose {hand.wager}')

            elif hand.value > self.dealer.hands[0].value:
                print(f'Hand holds, you win {hand.wager}')
                self.account(hand.wager * 2)

            else:
                print('Push')
                self.account(hand.wager)

    def hit(self, curr_hand):
        hit = self.deck.draw()
        curr_hand.cards += (hit,)
        print(f'{hit} ({curr_hand.value})')
        return True if curr_hand.bust else False
        
    def split(self, wager):
        curr_hand = int
        for hand in self.player.hands:
            if hand.active:
                curr_hand = self.player.hands.index(hand)
                break

        # create new player hand with second card from splitting hand
        self.player.add_hand(Hand(self.player.hands[curr_hand].cards[1], self.deck.draw(), wager))
        # knock off new hands wager
        self.account(-wager)
        # replace curr_hand with the hand with same first and new second card 
        self.player.hands[curr_hand] = Hand(self.player.hands[curr_hand].cards[0], self.deck.draw(), wager)
    
    def account(self, amount):
        "handles settling arithmetic and passing updated stack labels"
        self.stack += amount
        self.labels['stack'] = Label(str(self.stack), self.width/6, (self.height/4) * 3, self.width/7, self.height/8)

    def draw(self):
        "called in each subloop: deal, hitting etc."
        self._screen.fill("darkgreen")

        for i, hand in enumerate(self.player.hands):
            hand.rect = pygame.Rect(i * self.width/len(self.player.hands), self.height/2, 50, 50)
            hand.draw(self._screen, self.card_w, self.card_h)

        for hand in self.player.hands: # focus on active hand
            if hand.active:
                focus = pygame.Rect(hand.rect.x - 2, hand.rect.y - 2, 4 + (len(hand.cards) * self.card_w), 4 + self.card_h)
                pygame.draw.rect(self._screen, color="yellow", rect=focus, width=2)
                break


        for hand in self.dealer.hands:
            hand.rect = pygame.Rect(0, self.height/8, 50, 50)
            hand.draw(self._screen, self.card_w, self.card_h)

        for label in self.labels.values():
            label.draw(self._screen)

        for button in self.buttons.values():
            button.draw(self._screen)

        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()