import pygame
from BaseButton import Button
from MusicSlider import Slider
#from Guardar import cargar_matriz

button_size = (200, 70)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
OVER = (225, 209, 65)
DARKBLUE = (10, 0, 255)

def menuCarga(window, window_size, font, clock, img):

    panel = pygame.Surface(window_size)
    fg_text = font.render("SELECT PUZZLE", WHITE, None, 0, 0, window_size[0]//14)
    bg_text = font.render("SELECT PUZZLE", BLACK, None, 0, 0, window_size[0]//14)

    panel.blits(blit_sequence=((img, (0, 0)), (bg_text[0], ((window_size[0] - bg_text[1].width) // 2, 55)), (fg_text[0], ((window_size[0] - fg_text[1].width) // 2, 50))))

    volume_slider = Slider(DARKBLUE, WHITE, 70, 30, 150, 20, 0, 1, pygame.mixer.music.get_volume())
    sub_img = img.subsurface((60, 30, 170, 20))

    quit_button = Button(WHITE, (window_size[0]//2) - button_size[0]//2, window_size[1] - button_size[1] * 1.5, button_size[0], button_size[1], "GO BACK")

    for i in range(6):
        if i <= 2:
            rect = pygame.Rect((window_size[0]//2 - window_size[0]//10) + window_size[0]//4 * (i - 1), window_size[1]//3 - window_size[1]//8, window_size[0]//5, window_size[0]//5)
            pygame.draw.rect(panel, WHITE, rect)
        
        else: 
            rect = pygame.Rect((window_size[0]//2 - window_size[0]//10) + window_size[0]//4 * (i - 4), window_size[1]//3 + window_size[1]//5, window_size[0]//5, window_size[0]//5)
            pygame.draw.rect(panel, WHITE, rect)

    running = True
    while running:
        clock.tick(60)
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if quit_button.isOver(pos):
                    running = False

            elif event.type == pygame.MOUSEMOTION:
                if quit_button.isOver(pos):
                    quit_button.color = OVER

                else:
                    quit_button.color = WHITE


            volume_slider.handle_event(event)
            panel.blit(sub_img, (60, 30))

        volume_slider.val = pygame.mixer.music.get_volume()
        volume_slider.draw(panel)
        quit_button.draw(panel, True)
        window.blit(panel, (0, 0))
        pygame.display.flip()