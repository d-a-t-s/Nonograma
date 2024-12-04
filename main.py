import pygame, pygame.freetype, sys
from MenuBool import menuBool
from ColorNono import game
from BaseButton import Button
from MusicSlider import Slider
from MenuCarga import menuCarga

def main_menu():
    clock = pygame.time.Clock()
    pygame.mixer.music.play(-1, 0, 100)
    pygame.mixer.music.set_volume(0.2)
    volume_slider = Slider(DARKBLUE, WHITE, 70, 30, 150, 20, 0, 1, pygame.mixer.music.get_volume())

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if start_button.isOver(pos):
                    menuBool(window, window_size, font, clock, img_menu)
                    window.blits(blit_sequence=((img_menu, (0, 0)), (bg_text[0], ((window_size[0] - bg_text[1].width) // 2, (window_size[1] // 8) + 5)), (fg_text[0], ((window_size[0] - fg_text[1].width) // 2, window_size[1] // 8))))

                elif colored_button.isOver(pos):
                    game(window, window_size, font, clock)
                    window.blits(blit_sequence=((img_menu, (0, 0)), (bg_text[0], ((window_size[0] - bg_text[1].width) // 2, (window_size[1] // 8) + 5)), (fg_text[0], ((window_size[0] - fg_text[1].width) // 2, window_size[1] // 8))))

                elif load_button.isOver(pos):
                    menuCarga(window, window_size, font, clock, img_menu)
                    window.blits(blit_sequence=((img_menu, (0, 0)), (bg_text[0], ((window_size[0] - bg_text[1].width) // 2, (window_size[1] // 8) + 5)), (fg_text[0], ((window_size[0] - fg_text[1].width) // 2, window_size[1] // 8))))

                elif exit_button.isOver(pos):
                    running = False
                
            elif event.type == pygame.MOUSEMOTION:
                if start_button.isOver(pos):
                    start_button.color = OVER

                elif exit_button.isOver(pos):
                    exit_button.color = OVER

                elif load_button.isOver(pos):
                    load_button.color = OVER    

                elif colored_button.isOver(pos):
                    colored_button.color = OVER

                else:
                    start_button.color = WHITE
                    colored_button.color = WHITE
                    load_button.color = WHITE
                    exit_button.color = WHITE

            elif event.type == pygame.QUIT:
                running = False

            volume_slider.handle_event(event)
            window.blit(sub_img, (60, 30))

        volume_slider.val = pygame.mixer.music.get_volume()
        volume_slider.draw(window)
        start_button.draw(window, True)
        colored_button.draw(window, True)
        load_button.draw(window, True)
        exit_button.draw(window, True)
        pygame.display.flip()
    pygame.quit()

if not pygame.image.get_extended():
    print("Error")
    sys.exit()

pygame.init()

WHITE = (255, 255, 255)
OVER = (225, 209, 65)
DARKBLUE = (10, 0, 255)
BLACK = (0, 0, 0)

window_size = (1152, 864)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Interface test")

pygame.mixer.music.load("PKM_B-W_Dragon_Spiral_Tower_Music.mp3")

font = pygame.freetype.Font('upheavtt.ttf', 16)
bg_text = font.render("PIXEL PASSION", BLACK, None, 0, 0, 110)
fg_text = font.render("PIXEL PASSION", WHITE, None, 0, 0, 110)
img_menu = pygame.image.load('bg_menu.png').convert()
sub_img = img_menu.subsurface((60, 30, 170, 20))
window.blits(blit_sequence=((img_menu, (0, 0)), (bg_text[0], ((window_size[0] - bg_text[1].width) // 2, (window_size[1] // 8) + 5)), (fg_text[0], ((window_size[0] - fg_text[1].width) // 2, window_size[1] // 8))))

button_size = (200, 60)
start_button = Button(WHITE, (window_size[0]//2) - button_size[0]//2, (window_size[1]//2) - button_size[1]//2 - 60, button_size[0], button_size[1], "B / W")
colored_button = Button(WHITE, (window_size[0]//2) - button_size[0]//2, (window_size[1]//2) - button_size[1]//2 + 60, button_size[0], button_size[1], "COLORS")
load_button = Button(WHITE, (window_size[0]//2) - button_size[0]//2, (window_size[1]//2) - button_size[1]//2 + 180, button_size[0], button_size[1], "LOAD")
exit_button = Button(WHITE, (window_size[0]//2) - button_size[0]//2, (window_size[1]//2) - button_size[1]//2 + 300, button_size[0], button_size[1], "EXIT")
main_menu()