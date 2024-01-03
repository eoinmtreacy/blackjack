from objects import * 

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
