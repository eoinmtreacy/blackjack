import pygame
from pygame.locals import * 

from button import Button
from player import Player
from deck import Deck
from hand import Hand
from card import Card
from input import Input
from label import Label
from banker import Banker

# name_label = Label(NAME, 0, (HEIGHT/4) * 3 , WIDTH/7, HEIGHT/8)



# banker = Banker(STACK, WIDTH/7, (HEIGHT/4) * 3 , WIDTH/7, HEIGHT/8)

# NAME = take_input("red", screen, WIDTH/2, HEIGHT/2, 100, 40)
# STACK = take_input("blue", screen, WIDTH/2, HEIGHT/2, 100, 40)

# wager = int(take_input("green", screen, WIDTH/2, HEIGHT/2, 100, 40))


# menus = [banker, name_label, wager_label, hit_button, split_button, stand_button, double_button]

class Game:
    def __init__(self):
        pygame.init()
        self.size = self.width, self.height = 480, 300
        self._screen = pygame.display.set_mode((self.size))
        self._running = True
        self.player = Player("Player")
        self.dealer = Player("Dealer")
        self.deck = Deck(Card,8)
        self.buttons = {
            'hit': Button("hit", self.width/2, self.height/4 * 3, 30, 30, "red", "h"),
            'split': Button("split", self.width/2 + 30, self.height/4 * 3, 60, 30, "yellow", "s"),
            'stand': Button("stand", self.width/2 + 90, self.height/4 * 3, 60, 30, "grey", " "),
            'double': Button("double", self.width/2 + 150, self.height/4 * 3, 60, 30, "hotpink", "d")
        }
        self.menus = {
            'stack': Label('420', self.width/6, (self.height/4) * 3, self.width/7, self.height/8),
            'wager': Label('69', self.width/6*2, (self.height/4) * 3, self.width/7, self.height/8)
        }
    
    def draw(self):
        "called in each subloop: deal, hitting etc."
        self._screen.fill("darkgreen")
        for i, hand in enumerate(self.player.hands):
                for j, card in enumerate(hand.cards):
                    card.rect = pygame.Rect((i * self.width/len(self.player.hands)) + (j * 30), self.height/2, 30, 50)
                    card.draw(self._screen)

        for menu in self.menus.values():
            menu.draw(self._screen)

        for button in self.buttons.values():
            button.draw(self._screen)

        for hand in self.dealer.hands:
            for i, card in enumerate(hand.cards):
                card.rect = pygame.Rect(i * 30, 30, 30, 50)
                card.draw(self._screen)

        pygame.display.update()

    def on_execute(self):
        while(self._running):
            for event in pygame.event.get():
                self.on_event(event)
            blackjack = self.deal()
            if not blackjack:
                bust = self.hitting()
                if not bust:
                    self.dealer_play()
            self.settle()
        self.on_cleanup()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def deal(self):
        "first subloop add cards to hands and hands to player and dealer"
        print('deal')
        if len(self.deck.cards) != 0:
            self.player.hands, self.dealer.hands = [Hand(self.deck.draw(), self.deck.draw())], [Hand(self.deck.draw(), self.deck.draw())]
            self.draw()
            
            # if self.dealer.hands[0].value == 21 and self.player.hands[0].value != 21:
            #     print(f'Dealer wins, blackjack')
            #     return False
            # else:
            #     return True
        else:
            print("Deck is empty")

        return False # conditions later to reset deck halfway

    def hitting(self):
        "if not dealer blackjack (peak), await user input"
        print('hitting')
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
                            if event.unicode == "s" or event.unicode == "S":
                                # self.split(banker, screen)
                                break

                            # handle doubling: ...if event.unicode == "d" etc 
                            
                            if event.key == pygame.K_RETURN:
                                hand.active = False
                                break

    def dealer_play(self):
        while True:
            self.screen.fill('pink')
            self.draw()
            pygame.display.update()
            pygame.time.wait(1000)
            
            if self.dealer.hands[0].value < 17:
                hit = self.deck.draw()
                self.dealer.hands[0].cards += (hit,)
            else:
                break

        print("finished!", self.dealer.hands[0].value)
        # while any hands active keep playing
        if any([hand.active for hand in self.player.hands]):
            pass
        else:
            # all hands.bust == true
            if all([hand.bust() for hand in self.player.hands]):
                print("True")
                return True
            else:
                # at least one not bust 
                print("False")
                return False
        
        self.draw()
        pygame.display.update()
        
    def settle(self):
        "handles wager and banker methods for each hand in player hands"

        for hand in self.player.hands:
            self.screen.fill("blue")
            pygame.time.wait(1000) # so player can see what's going on
            self.draw()

            if hand.bust():
                print(f'Hand busted, you lose {hand.wager}')

            elif self.dealer.hands[0].bust():
                print(f'Dealer bust, hand wins {hand.wager}')

                self.account(hand.wager * 2)
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
    
    def account(self, amount):
        self.value = str(int(self.value) + amount)
        self.img = self.font.render(self.value, True, self.color)

    def on_cleanup(self):
        pygame.quit()