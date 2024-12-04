import pygame
from BaseButton import Button
from MusicSlider import Slider

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
OVER = (225, 209, 65)
DARKBLUE = (10, 0, 255)

def menuEsc(window, width, height, font, clock):

    panel = pygame.Surface((width, height), pygame.SRCALPHA)
    fg_text = font.render("PAUSE MENU", WHITE, None, 0, 0, width//14)
    bg_text = font.render("PAUSE MENU", BLACK, None, 0, 0, width//14)

    menu = pygame.Surface((width//2, height - 50))
    img_menu = pygame.image.load('bg_menu.png')
    menu.blit(img_menu, (0, 0))
    menu.blits(blit_sequence=((bg_text[0], ((menu.get_width() - bg_text[1].width) // 2, 55)), (fg_text[0], ((menu.get_width() - fg_text[1].width) // 2, 50))))
    sub_img = img_menu.subsurface((menu.get_width()//2 + 10, menu.get_height() - 20, 170, 20))

    button_size = (width//6, height//8)
    resume_button = Button(WHITE, (width - button_size[0])//2, button_size[1]*2, button_size[0], button_size[1], "RESUME")
    save_button = Button(WHITE, (width - button_size[0])//2, button_size[1]*3.5, button_size[0], button_size[1], "SAVE")
    quit_button = Button(WHITE, (width - button_size[0])//2, button_size[1]*5, button_size[0], button_size[1], "QUIT")
    volume_slider = Slider(DARKBLUE, WHITE, menu.get_width()//2 + 10, menu.get_height() - 40, 150, 20, 0, 1, pygame.mixer.music.get_volume())
    
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

                elif save_button.isOver(pos):
                    return True

                elif quit_button.isOver(pos):
                    running = False
                    return True
            
            elif event.type == pygame.MOUSEMOTION:
                if resume_button.isOver(pos):
                    resume_button.color = OVER

                elif quit_button.isOver(pos):
                    quit_button.color = OVER

                elif save_button.isOver(pos):
                    save_button.color = OVER

                else:
                    resume_button.color = WHITE
                    save_button.color = WHITE
                    quit_button.color = WHITE

            volume_slider.handle_event(event)
            panel.blit(sub_img, (menu.get_width()//2, menu.get_height() - 40))
        
        volume_slider.val = pygame.mixer.music.get_volume()
        volume_slider.draw(panel)
        resume_button.draw(panel, True)
        save_button.draw(panel, True)
        quit_button.draw(panel, True)
        window.blit(panel, (0, 0))
        pygame.display.flip()