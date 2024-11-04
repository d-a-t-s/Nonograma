import pygame, pygame.freetype
from BaseButton import Button

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (225, 209, 65)

def win(window, window_size, font, clock):
    
    panel = pygame.Surface(window_size, pygame.SRCALPHA)
    win = pygame.Surface((window_size[0] // 2, window_size[1] // 2), pygame.SRCALPHA)
    win.fill((0, 0, 0, 0))
    bg_win = font.render("WIN", (173, 146, 50), None, 0, 0, window_size[0] // 4)
    fg_win = font.render("WIN", YELLOW, None, 0, 0, window_size[0] // 4)
    win.blits(blit_sequence=((bg_win[0], ((win.get_width() - bg_win[1].width) // 2 - 5, 15)), (fg_win[0], ((win.get_width() - fg_win[1].width) // 2, 20))))
    
    button_size = (window_size[0]//6, window_size[1]//8)
    resume_button = Button(WHITE, (window_size[0] // 2 + button_size[0] * 0.2), button_size[1] * 4.5, button_size[0], button_size[1], "RESUME")
    quit_button = Button(WHITE, (window_size[0] // 2 - button_size[0] * 1.2), button_size[1] * 4.5, button_size[0], button_size[1], "QUIT")

    panel.fill((0, 0, 0, 3))
    panel.blit(win, (window_size[0] // 4, window_size[1] // 4))
    

    running = True
    while running:
        clock.tick(60)
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if resume_button.isOver(pos):
                    running = False

                elif quit_button.isOver(pos):
                    running = False
                    return True
            
            elif event.type == pygame.MOUSEMOTION:
                if resume_button.isOver(pos):
                    resume_button.color = YELLOW

                elif quit_button.isOver(pos):
                    quit_button.color = YELLOW

                else:
                    resume_button.color = WHITE
                    quit_button.color = WHITE

        resume_button.draw(panel, True)
        quit_button.draw(panel, True)
        window.blit(panel, (0, 0))
        pygame.display.flip()