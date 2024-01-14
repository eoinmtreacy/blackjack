import asyncio
import pygame
from pygame.locals import *
from library import *

pygame.init()
pygame.event.set_allowed([QUIT, KEYDOWN])

CLOCK = pygame.time.Clock()
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

def account(stack, amount):
    "handles settling arithmetic and passing updated stack labels"
    stack += amount
    LABELS['stack'] = Label(str(stack), WIDTH/16*4, HEIGHT/9*7.5, WIDTH/4, WIDTH/64*6)
    return stack

INPUT = Input(WIDTH/16*6, HEIGHT/9*3, WIDTH/16*4, WIDTH/64*6)
BET = Button("bet", WIDTH/16*10.2, HEIGHT/9*3, WIDTH, " ")

def draw(*args):
    "draw pieces for each subloop with variable args for input, bet button etc."
    SCREEN.blit(BACKGROUND, (0,0))

    for i, hand in enumerate(PLAYER.hands):
        hand.rect = pygame.Rect(i * WIDTH/len(PLAYER.hands) + WIDTH/16, HEIGHT/9*5.5, 50, 50)
        hand.draw(SCREEN, CARD_WIDTH, CARD_HEIGHT)

    for hand in PLAYER.hands: # focus on active hand
        if hand.active:
            focus = pygame.Rect(hand.rect.x - 4, hand.rect.y - 4, 8 + (len(hand.cards) * CARD_WIDTH), 8 + CARD_HEIGHT)
            pygame.draw.rect(SCREEN, color="yellow", rect=focus, width=4)
            break

    for hand in DEALER.hands:
        hand.rect = pygame.Rect(WIDTH/16, HEIGHT/8, 50, 50)
        hand.draw(SCREEN, CARD_WIDTH, CARD_HEIGHT)

    for label in LABELS.values():
        label.draw(SCREEN)

    for button in BUTTONS.values():
        button.draw(SCREEN)

    for each in args:
        each.draw(SCREEN)

    pygame.display.update()

def hit(curr_hand):
    "add card to hand"
    hit = DECK.draw()
    curr_hand.cards += (hit,)
    return True if curr_hand.bust else False
        
def split(wager):
    "append second hands to self.player.hands using one card from splitting hand"
    global STACK
    for hand in PLAYER.hands:
        if hand.active:
            curr_hand = PLAYER.hands.index(hand)
            break
    # create new player hand with second card from splitting hand
    PLAYER.hands.append(Hand(PLAYER.hands[curr_hand].cards[1], DECK.draw(), label_size=CARD_WIDTH, wager=wager))
    # knock off new hands wager
    STACK = account(STACK, -wager)
    # replace curr_hand with the hand with same first and new second card 
    PLAYER.hands[curr_hand] = Hand(PLAYER.hands[curr_hand].cards[0], DECK.draw(), label_size=CARD_WIDTH, wager=wager)

STATES = {
    'wager': False,
    'deal': False,
    'hitting': False,
    'dealer_play': False,
    'settle': False
    }

async def main():
    global STACK
    game_running = True
    STATES['wager'] = True

    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                pygame.quit()

            if STATES['wager']:
                if event.type == pygame.KEYDOWN:
                        output = INPUT.handle_type(event)
                        if event.key == pygame.K_RETURN and output != '':
                            if int(output) > STACK:
                                #TODO can't bet that much animation, input shake or something
                                pass
                            else:
                                WAGER = int(output)
                                STATES['wager'] = False
                                STATES['deal'] = True

            if STATES['hitting']:
                for hand in PLAYER.hands:
                    if hand.active: 
                        if event.type == pygame.KEYDOWN:

                            if event.unicode == "h" or event.unicode == "H":
                                hit(hand)
                                break
                            
                            # conditions for split: key press, only two cards in hand and both the same value
                            if (event.unicode == "s" or event.unicode == "S"): #  and len(hand.cards) == 2 and hand.cards[0].value == hand.cards[1].value:
                                if WAGER <= STACK:
                                    split(WAGER)
                                    break
                                else:
                                    print("You don't have enough to split")
                            
                            if (event.unicode == "d" or event.unicode == "D"):
                                if WAGER <= STACK:
                                    hand.wager *= 2
                                    hand.label.update("$" + str(WAGER * 2))
                                    hand.active = False
                                    STACK = account(STACK, -WAGER)
                                    print(STACK)
                                    hit(hand)
                                    break
                                else:
                                    print("You don't have enough to double")

                            if event.key == pygame.K_RETURN:
                                hand.active = False
                                break

                if not any([hand.active for hand in PLAYER.hands]):
                    STATES['hitting'] = False
                    DEALER.hands[0].cards[0].hidden = False
                    if all([hand.bust for hand in PLAYER.hands]):
                        STATES['settle'] = True

                    else:
                        STATES['dealer_play'] = True

        if STATES['deal']:
            blackjack = False

            if len(DECK.cards) > 52*4:
                PLAYER.hands, DEALER.hands = [Hand(DECK.draw(), DECK.draw(), label_size=CARD_WIDTH, wager=WAGER)], [Hand(DECK.draw(True), DECK.draw(), label_size=CARD_WIDTH)]
                STACK = account(STACK, -WAGER)
                print(STACK)
                draw()
                pygame.time.wait(1000)
                
                if DEALER.hands[0].value == 21 and PLAYER.hands[0].value != 21:
                    blackjack = True
                elif DEALER.hands[0].value != 21 and PLAYER.hands[0].value == 21:
                    blackjack = True
                elif DEALER.hands[0].value == 21 and PLAYER.hands[0].value == 21:
                    blackjack = True

            STATES['deal'] = False
            if not blackjack:
                STATES['hitting'] = True
            else:
                pygame.time.wait(1000)
                STATES['settle'] = True

        if STATES['dealer_play']:
            while DEALER.hands[0].value < 17:
                draw()
                pygame.time.wait(1000)
                hit(DEALER.hands[0]) 
            STATES['dealer_play'] = False
            STATES['settle'] = True

        if STATES['settle']:
            for hand in PLAYER.hands:
                if hand.bust:
                    pass

                elif DEALER.hands[0].bust:
                    STACK = account(STACK, hand.wager * 2)
                    hand.label.update("+$" + str(hand.wager * 2), color="green")

                elif hand.value == 21 and len(hand.cards) == 2 and DEALER.hands[0].value != 21:
                    STACK = account(STACK, hand.wager * 3)
                    hand.label.update("+$" + str(hand.wager * 3), color="yellow")

                elif DEALER.hands[0].value > hand.value:
                    hand.label.update("$0", color='crimson')

                elif hand.value > DEALER.hands[0].value:
                    STACK = account(STACK, hand.wager * 2)
                    hand.label.update("+$" + str(hand.wager * 2), color="green")

                else:
                    STACK = account(STACK, hand.wager)
                    hand.label.update("$0", color='lightgrey')

                draw()
                pygame.time.wait(1000)

            STATES['settle'] = False
            STATES['wager'] = True

        draw(INPUT, BET) if STATES['wager'] else draw()
        await asyncio.sleep(0)

asyncio.run(main())