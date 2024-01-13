import pygame
from pygame.locals import *

from library import *

pygame.init()



SIZE = WIDTH, HEIGHT = 1200, 700
CARD_SIZE = CARD_WIDTH, CARD_HEIGHT = WIDTH/13, HEIGHT/5
SCREEN = pygame.display.set_mode((SIZE))
BACKGROUND = pygame.transform.scale(pygame.image.load('./src/background_bluf.png'), SIZE)
PLAYER = Player("Player")
DEALER = Player("Dealer")
DECK = Deck(Card,8)

BUTTONS = {
    'hit': Button("hit", WIDTH/64*33, HEIGHT/9*7.5, WIDTH, "h"),
    'stand': Button("stand", WIDTH/64*41, HEIGHT/9*7.5, WIDTH, " "),
    'split': Button("split", WIDTH/64*49, HEIGHT/9*7.5, WIDTH, "s"),
    'double': Button("double", WIDTH/64*57, HEIGHT/9*7.5, WIDTH, "d"),
}

STACK = 1000 #stack tied to game, not player, up for debate, not sure if more than one player in needed
LABELS = {
    'stack': Label(str(STACK), WIDTH/16*4, HEIGHT/9*7.5, WIDTH/4, WIDTH/64*6)
}

INPUT = Input(WIDTH/16*6, HEIGHT/9*3, WIDTH/16*4, WIDTH/64*6)
BET = Button("bet", WIDTH/16*10.2, HEIGHT/9*3, WIDTH, " ")

def draw(*args):
    "draw pieces for each subloop with variable args for input, bet button etc."
    SCREEN.blit(BACKGROUND, (0,0))

    # for i, hand in enumerate(self.player.hands):
    #     hand.rect = pygame.Rect(i * self.width/len(self.player.hands) + self.width/16, self.height/9*5.5, 50, 50)
    #     hand.draw(self._screen, self.card_w, self.card_h)

    # for hand in self.player.hands: # focus on active hand
    #     if hand.active:
    #         focus = pygame.Rect(hand.rect.x - 4, hand.rect.y - 4, 8 + (len(hand.cards) * self.card_w), 8 + self.card_h)
    #         pygame.draw.rect(self._screen, color="yellow", rect=focus, width=4)
    #         break

    # for hand in self.dealer.hands:
    #     hand.rect = pygame.Rect(self.width/16, self.height/8, 50, 50)
    #     hand.draw(self._screen, self.card_w, self.card_h)

    for label in LABELS.values():
        label.draw(SCREEN)

    for button in BUTTONS.values():
        button.draw(SCREEN)

    for each in args:
        each.draw(SCREEN)

    pygame.display.update()

STATES = {
    'wager': False,
    'deal': False,
    'hitting': False,
    'dealer_play': False,
    'settle': False
    }

def main():
    game_running = True
    STATES['wager'] = True

    while game_running:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                    pygame.quit()

        if STATES['wager']:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                        print("fire")
                        output = INPUT.handle_type(event)
                        if event.key == pygame.K_RETURN and output != '':
                            if int(output) > STACK:
                                #TODO can't bet that much animation, input shake or something
                                pass
                            else:
                                STATES['wager'] = False
                                STATES['deal'] = True
            
            draw(INPUT, BET)

        if STATES['deal']:
             draw()

main()
