import pygame
from pygame.locals import * 

from deck import (Deck, Card)
from hand import (Player, Hand)
from input import Input
from button import Button
from label import Label

class Game:
    def __init__(self):
        pygame.init()
        self.size = self.width, self.height = 1200, 700
        self.card_w, self.card_h = self.width/13, self.height/5

        self._screen = pygame.display.set_mode((self.size))
        self.background = pygame.transform.scale(pygame.image.load('./src/background_bluf.png'), self.size)
        self._running = True

        self.player = Player("Player")
        self.dealer = Player("Dealer")
        self.deck = Deck(Card,8)

        self.buttons = {
            'hit': Button("hit", self.width/64*33, self.height/9*7.5, self.width, "h"),
            'stand': Button("stand", self.width/64*41, self.height/9*7.5, self.width, " "),
            'split': Button("split", self.width/64*49, self.height/9*7.5, self.width, "s"),
            'double': Button("double", self.width/64*57, self.height/9*7.5, self.width, "d"),
        }

        self.stack = 1000 #stack tied to game, not player, up for debate, not sure if more than one player in needed
        self.labels = {
            'stack': Label(str(self.stack), self.width/16*4, self.height/9*7.5, self.width/4, self.width/64*6)
        }
    
    def play(self):
        "main loop, subloops return boolean pairs for _running and logic branching respectively"
        while(self._running):
            self._running, wager = self.get_wager()
            if wager:
                blackjack = self.deal(wager)
                if not blackjack:
                    self._running, bust = self.hitting(wager)
                    self.dealer.hands[0].cards[0].hidden = False # unhide dealer hole card at end of hitting
                    if not bust:
                        self.dealer_play()
                self.dealer.hands[0].cards[0].hidden = False # unhide dealer hole card if blackjack
                self.settle()
            self.draw()
            pygame.time.wait(1000)
        pygame.quit()

    def get_wager(self):
        "get user bet input, only accepts integers (as strings), returns wager as int"
        new_input = Input(self.width/16*6, self.height/9*3, self.width/16*4, self.width/64*6)
        bet_button = Button("bet", self.width/16*10.2, self.height/9*3, self.width, " ")
        self.buttons['bet'] = bet_button

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return (False, False)
                elif event.type == pygame.KEYDOWN:
                    output = new_input.handle_type(event)
                    if event.key == pygame.K_RETURN and output != '':
                        if int(output) > self.stack:
                            #TODO can't bet that much animation, input shake or something
                            pass
                        else:
                            del(self.buttons['bet'])
                            return (True, int(output))
            self.draw(new_input, bet_button)

    def deal(self, wager):
        "add cards to hands and hands to player and dealer, returns False if neither player blackjack (21) else True"
        if len(self.deck.cards) != 0:
            self.player.hands, self.dealer.hands = [Hand(self.deck.draw(), self.deck.draw(), wager)], [Hand(self.deck.draw(True), self.deck.draw())]
            self.account(-wager)
            self.draw()
            pygame.time.wait(1000)
            
            if self.dealer.hands[0].value == 21 and self.player.hands[0].value != 21:
                return True
            elif self.dealer.hands[0].value != 21 and self.player.hands[0].value == 21:
                return True
            elif self.dealer.hands[0].value == 21 and self.player.hands[0].value == 21:
                return True
            else:
                return False
            
            #TODO handle empty deck

    def hitting(self, wager):
        "if not dealer blackjack (peak), await user input"
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return (False, True) # return self._gamerunning, bust = False, True
                for hand in self.player.hands:
                    if hand.active: 
                        if event.type == pygame.KEYDOWN:

                            if event.unicode == "h" or event.unicode == "H":
                                self.hit(hand)
                                break
                            
                            # conditions for split: key press, only two cards in hand and both the same value
                            if (event.unicode == "s" or event.unicode == "S") and len(hand.cards) == 2 and hand.cards[0].value == hand.cards[1].value:
                                if wager <= self.stack:
                                    self.split(wager)
                                    break
                                else:
                                    print("You don't have enough to split")
                            
                            if (event.unicode == "d" or event.unicode == "D"):
                                if wager <= self.stack:
                                    hand.wager *= 2
                                    hand.label.update(str(wager * 2) + "$")
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
            if not any([hand.active for hand in self.player.hands]):
                return (True, True) if all([hand.bust for hand in self.player.hands]) else (True, False)
            
            self.draw()

    def dealer_play(self):
        "dealer stands on 17"

        while True:
            self.draw()
            pygame.time.wait(1000)
            if self.dealer.hands[0].value < 17:
                self.hit(self.dealer.hands[0]) 
            else:
                break
            
    def settle(self):
        "for each player hand settles up with dealer"
        for hand in self.player.hands:
            if hand.bust:
                pass

            elif self.dealer.hands[0].bust:
                self.account(hand.wager * 2)
                hand.label.update("+" + str(hand.wager * 2), color="green")

            elif hand.value == 21 and len(hand.cards) == 2 and self.dealer.hands[0].value != 21:
                hand.label.update("+" + str(hand.wager * 3), color="yellow")

            elif self.dealer.hands[0].value > hand.value:
                hand.label.update("0", color='crimson')

            elif hand.value > self.dealer.hands[0].value:
                self.account(hand.wager * 2)
                hand.label.update("+" + str(hand.wager * 2), color="green")

            else:
                self.account(hand.wager)
                hand.label.update("0", color='lightgrey')
            
            self.draw()
            pygame.time.wait(1000)

    def hit(self, curr_hand):
        "add card to hand"
        hit = self.deck.draw()
        curr_hand.cards += (hit,)
        return True if curr_hand.bust else False
        
    def split(self, wager):
        "append second hands to self.player.hands using one card from splitting hand"
        for hand in self.player.hands:
            if hand.active:
                curr_hand = self.player.hands.index(hand)
                break
        # create new player hand with second card from splitting hand
        self.player.hands.append(Hand(self.player.hands[curr_hand].cards[1], self.deck.draw(), wager))
        # knock off new hands wager
        self.account(-wager)
        # replace curr_hand with the hand with same first and new second card 
        self.player.hands[curr_hand] = Hand(self.player.hands[curr_hand].cards[0], self.deck.draw(), wager)
    
    def account(self, amount):
        "handles settling arithmetic and passing updated stack labels"
        self.stack += amount
        self.labels['stack'] = Label(str(self.stack), self.width/16*4, self.height/9*7.5, self.width/4, self.width/64*6)

    def draw(self, *args):
        "draw pieces for each subloop with variable args for input, bet button etc."
        self._screen.blit(self.background, (0,0))

        for i, hand in enumerate(self.player.hands):
            hand.rect = pygame.Rect(i * self.width/len(self.player.hands) + self.width/16, self.height/9*5.5, 50, 50)
            hand.draw(self._screen, self.card_w, self.card_h)

        for hand in self.player.hands: # focus on active hand
            if hand.active:
                focus = pygame.Rect(hand.rect.x - 4, hand.rect.y - 4, 8 + (len(hand.cards) * self.card_w), 8 + self.card_h)
                pygame.draw.rect(self._screen, color="yellow", rect=focus, width=4)
                break

        for hand in self.dealer.hands:
            hand.rect = pygame.Rect(self.width/16, self.height/8, 50, 50)
            hand.draw(self._screen, self.card_w, self.card_h)

        for label in self.labels.values():
            label.draw(self._screen)

        for button in self.buttons.values():
            button.draw(self._screen)

        for each in args:
            each.draw(self._screen)

        pygame.display.update()