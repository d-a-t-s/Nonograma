import pygame
from BaseButton import Button

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
OVER = (225, 209, 65)

def menuEsc(window, width, height, font, clock):

    panel = pygame.Surface((width, height), pygame.SRCALPHA)
    fg_text = font.render("PAUSE MENU", WHITE, None, 0, 0, width//14)
    bg_text = font.render("PAUSE MENU", BLACK, None, 0, 0, width//14)

    menu = pygame.Surface((width//2, height - 50))
    img_menu = pygame.image.load('bg_menu.png')
    menu.blit(img_menu, (0, 0))
    menu.blits(blit_sequence=((bg_text[0], ((menu.get_width() - bg_text[1].width) // 2, 55)), (fg_text[0], ((menu.get_width() - fg_text[1].width) // 2, 50))))

    button_size = (width//6, height//8)
    resume_button = Button(WHITE, (width - button_size[0])//2, button_size[1]*2, button_size[0], button_size[1], "RESUME")
    quit_button = Button(WHITE, (width - button_size[0])//2, button_size[1]*6, button_size[0], button_size[1], "QUIT")
    
    panel.fill((50,50,50,10))
    panel.blit(menu, (width//4, 25))

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
                    resume_button.color = OVER

                elif quit_button.isOver(pos):
                    quit_button.color = OVER

                else:
                    resume_button.color = WHITE
                    quit_button.color = WHITE

        resume_button.draw(panel, True)
        quit_button.draw(panel, True)
        window.blit(panel, (0, 0))
        pygame.display.flip()