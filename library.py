import pygame
from pygame.locals import *
import time
from random import shuffle

class Input:
    def __init__(self, x, y, w, h):
        self.size = self.width, self.height = (w, h)
        self.pos = self.x, self.y = (x, y)
        self.rect = pygame.Rect(self.pos, self.size)
        self.text = ""
        self.font = pygame.font.Font('font.ttf', int(self.height * 0.7))
        self.img = self.font.render(self.text, True, "white")
        self.border = pygame.image.load('./src/input.png')
        self.active = True

    def draw(self, screen):
        center_x, center_y = self.rect.center # find center of input rect
        img_x, img_y = self.img.get_size() # find the size of the text
        screen.blit(self.img, (center_x - img_x/2, center_y - img_y/2)) # blit to center
        screen.blit(pygame.transform.scale(self.border, self.size), self.rect) # blit to center
        pygame.draw.rect(screen, "white", self.rect, -1)

    def handle_type(self, event):
        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.unicode in '0123456789':
                    self.text += event.unicode
                # Re-render the text.
                self.img = self.font.render(self.text, True, "white")

class Button:
    def __init__(self, name, x, y, w, on_click):
        self.name = name
        self.size = self.width, self.height = w/64*6, w/64*6
        self.rect = pygame.Rect((x, y), (self.size))
        # self.font = pygame.font.SysFont('Helvetica', 24)
        self.img = pygame.image.load(f'./src/buttons/{name}.png')
        self.on_click = on_click
    
    def draw(self, screen):
        screen.blit(pygame.transform.scale(self.img, (self.width, self.height)), self.rect)
        pygame.draw.rect(screen, "grey", self.rect, -1)
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

class Label:
    "found as a Hand attribute for individual wagers or Game attribute for stack balance"
    def __init__(self, value, x=0, y=0, w=0, h=0, color='white'):
        self.value = "$" + value
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.font = pygame.font.Font("font.ttf", int(h * 0.8))
        self.img = self.font.render(self.value, True, self.color)

    def draw(self, screen):
        center_x, center_y = self.rect.center # find center of input rect
        img_x, img_y = self.img.get_size()
        screen.blit(self.img, (center_x - img_x/2, center_y - img_y/2.3)) # center typed input by taking half the size away from the center
        pygame.draw.rect(screen, self.color, self.rect, -1)

    def update(self, value, color="white"):
        self.value, self.color = value, color
        self.img = self.font.render(self.value, True, self.color)

class Card:
    def __init__(self, suit, value, img, back, hidden=False):
        self.hidden = hidden
        self.suits = ("clubs", "diamonds", "hearts", "spades")
        self.values = (None, "ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king")
        self.suit = self.suits[suit]
        self.value = self.values[value]
        self.rect = None # rect handled by game.draw()
        self.color = "white"
        self.img = img
        self.back = back
                                            
    def draw(self, screen, card_w, card_h):
        if not self.hidden:
            screen.blit(pygame.transform.scale(self.img, (card_w, card_h)), self.rect)
            pygame.draw.rect(screen, self.color, self.rect, -1)
        
        else:
            screen.blit(pygame.transform.scale(self.back, (card_w, card_h)), self.rect)
            pygame.draw.rect(screen, self.color, self.rect, -1)

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

class Player:
    def __init__(self, name):
        self.name = name
        self.hands = []

class Hand:
    def __init__(self, card1, card2, label_size, wager = 0, active = True):
        self.cards = (card1, card2)
        self.wager = wager
        self.active = active
        self.label = Label(str(self.wager), w=label_size, h=label_size)
    
    def draw(self, screen, card_w, card_h):
        if self.wager: # stops wager label drawing on dealer cards
            self.label.rect = Rect(self.rect.x, self.rect.y - card_w, card_w, card_w) # wager label, reference rect via game.draw()
            self.label.draw(screen)
        for c, card in enumerate(self.cards):
            card.rect = Rect(self.rect.x + c * card_w, self.rect.y, card_w, card_h)
            card.draw(screen, card_w, card_h)

    @property
    def value(self):
        value = 0
        for card in self.cards:
            add = 10 if card.values.index(card.value) > 10 else card.values.index(card.value)
            value += add

        if value + 10 < 22:
            aces = [card.value for card in self.cards].count("ace")
            for ace in range(aces):
                value += 10
                if value + 10 > 21:
                    break
            
        return value
    
    @property
    def bust(self):
        if self.value > 21:
            self.active = False
            self.label = Label("0", color='crimson')
            return True
        else:
            return False

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
            self.player.hands, self.dealer.hands = [Hand(self.deck.draw(), self.deck.draw(), label_size=self.card_w, wager=wager)], [Hand(self.deck.draw(True), self.deck.draw(), label_size=self.card_w)]
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
                            if (event.unicode == "s" or event.unicode == "S"): #  and len(hand.cards) == 2 and hand.cards[0].value == hand.cards[1].value:
                                if wager <= self.stack:
                                    self.split(wager)
                                    break
                                else:
                                    print("You don't have enough to split")
                            
                            if (event.unicode == "d" or event.unicode == "D"):
                                if wager <= self.stack:
                                    hand.wager *= 2
                                    hand.label.update("$" + str(wager * 2))
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
                hand.label.update("+$" + str(hand.wager * 2), color="green")

            elif hand.value == 21 and len(hand.cards) == 2 and self.dealer.hands[0].value != 21:
                self.account(hand.wager * 3)
                hand.label.update("+$" + str(hand.wager * 3), color="yellow")

            elif self.dealer.hands[0].value > hand.value:
                hand.label.update("$0", color='crimson')

            elif hand.value > self.dealer.hands[0].value:
                self.account(hand.wager * 2)
                hand.label.update("+$" + str(hand.wager * 2), color="green")

            else:
                self.account(hand.wager)
                hand.label.update("$0", color='lightgrey')

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
        self.player.hands.append(Hand(self.player.hands[curr_hand].cards[1], self.deck.draw(), label_size=self.card_w, wager=wager))
        # knock off new hands wager
        self.account(-wager)
        # replace curr_hand with the hand with same first and new second card 
        self.player.hands[curr_hand] = Hand(self.player.hands[curr_hand].cards[0], self.deck.draw(), label_size=self.card_w, wager=wager)
    
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

