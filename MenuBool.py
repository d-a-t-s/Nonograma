import pygame
from NonoDef import game
from BaseButton import Button

button_size = (200, 70)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
OVER = (225, 209, 65)

def menuBool(window, window_size, font, clock):

    panel = pygame.Surface((window_size[0], window_size[1]))
    img_menu = pygame.image.load('bg_menu.png')
    fg_text = font.render("SELECT SIZE", WHITE, None, 0, 0, window_size[0]//14)
    bg_text = font.render("SELECT SIZE", BLACK, None, 0, 0, window_size[0]//14)

    panel.blits(blit_sequence=((img_menu, (0, 0)), (bg_text[0], ((window_size[0] - bg_text[1].width) // 2, 55)), (fg_text[0], ((window_size[0] - fg_text[1].width) // 2, 50))))


    button_5 = Button(WHITE, (window_size[0]//2) - button_size[0]//2, (window_size[1]//2) - button_size[1]//2 - 170, button_size[0], button_size[1], "5 X 5")
    button_10 = Button(WHITE, (window_size[0]//2) - button_size[0]//2, (window_size[1]//2) - button_size[1]//2 - 70, button_size[0], button_size[1], "10 X 10")
    button_15 = Button(WHITE, (window_size[0]//2) - button_size[0]//2, (window_size[1]//2) - button_size[1]//2 + 30, button_size[0], button_size[1], "15 X 15")
    button_20 = Button(WHITE, (window_size[0]//2) - button_size[0]//2, (window_size[1]//2) - button_size[1]//2 + 130, button_size[0], button_size[1], "20 X 20")
    quit_button = Button(WHITE, (window_size[0]//2) - button_size[0]//2, (window_size[1]//2) - button_size[1]//2 + 300, button_size[0], button_size[1], "GO BACK")

    running = True
    while running:
        clock.tick(60)
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if button_5.isOver(pos):
                    game(window, window_size, font, clock, 5,5)
                    running = False

                elif button_10.isOver(pos):
                    game(window, window_size, font, clock, 10,10)
                    running = False

                elif button_15.isOver(pos):
                    game(window, window_size, font, clock, 15,15)
                    running = False

                elif button_20.isOver(pos):
                    game(window, window_size, font, clock, 20,20)
                    running = False

                elif quit_button.isOver(pos):
                    running = False
            
            elif event.type == pygame.MOUSEMOTION:
                if button_5.isOver(pos):
                    button_5.color = OVER

                elif button_10.isOver(pos):
                    button_10.color = OVER

                elif button_15.isOver(pos):
                    button_15.color = OVER

                elif button_20.isOver(pos):
                    button_20.color = OVER

                elif quit_button.isOver(pos):
                    quit_button.color = OVER

                else:
                    button_5.color = WHITE
                    button_10.color = WHITE
                    button_15.color = WHITE
                    button_20.color = WHITE
                    quit_button.color = WHITE

        button_5.draw(panel, True)
        button_10.draw(panel, True)
        button_15.draw(panel, True)
        button_20.draw(panel, True)
        quit_button.draw(panel, True)

        window.blit(panel, (0, 0))
        pygame.display.flip()