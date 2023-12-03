from objects import * 

def take_input(color, screen, x, y, w, h):

    new_input = Input("red", x, y, w, h)

    while True:
        screen.fill("grey")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

            output = new_input.handle_type(event)

            if event.type == pygame.K_RETURN:
                print(output)
                return output

        new_input.draw(screen)
        
        pygame.display.update()
