from objects import *
from input import *
from hitting import *
from dealer_play import *

WIDTH, HEIGHT = 480, 300

pygame.init()

screen = pygame.display.set_mode((WIDTH,HEIGHT))

game_running = True

while game_running:

    NAME = take_input("red", screen, WIDTH/2, HEIGHT/2, 100, 40)
    STACK = take_input("blue", screen, WIDTH/2, HEIGHT/2, 100, 40)

    # game object takes player name, stack and no. of decks
    game = Game(NAME, int(STACK), 1)

    name_label = Label(NAME, 0, (HEIGHT/4) * 3 , WIDTH/7, HEIGHT/8)

    # stack label reads from player object not from global so updates dynamically 
    stack_label = Label(str(game.player.stack), WIDTH/6, (HEIGHT/4) * 3, WIDTH/7, HEIGHT/8, STACK)

    hit_button = Button("hit", WIDTH/2, HEIGHT/4 * 3, 30, 30, "red", "h")
    split_button = Button("split", WIDTH/2 + 30, HEIGHT/4 * 3, 60, 30, "yellow", "s")
    stand_button = Button("stand", WIDTH/2 + 90, HEIGHT/4 * 3, 60, 30, "grey", " ")
    double_button = Button("double", WIDTH/2 + 150, HEIGHT/4 * 3, 60, 30, "hotpink", "d")
    

    # game_loop
    while True:
        wager = take_input("green", screen, WIDTH/2, HEIGHT/2, 100, 40)
        wager_label = Label(str(wager), WIDTH/6*2, (HEIGHT/4) * 3, WIDTH/7, HEIGHT/8)
        menus = [stack_label, name_label, wager_label, hit_button, split_button, stand_button, double_button]
        if not game.deal(wager):
            bust = hitting(game, screen, WIDTH, HEIGHT, menus)
            print(bust, "main.py")
            if not bust:
                dealer_play(game, screen, WIDTH, HEIGHT, menus[:3])
            else:
                pass

        # dealer play 
        # stands at 17
        # need to implement cards hide 

pygame.quit()