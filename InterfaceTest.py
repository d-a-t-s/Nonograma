import pygame, pygame.freetype, sys
from MenuBool import menuBool
from BaseButton import Button

def main_menu():
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONUP:
                if start_button.isOver(pos):
                    menuBool(window, window_size, font, clock)
                    window.blits(blit_sequence=((img_menu, (0, 0)), (bg_text[0], ((window_size[0] - bg_text[1].width) // 2, (window_size[1] // 8) + 5)), (fg_text[0], ((window_size[0] - fg_text[1].width) // 2, window_size[1] // 8))))

                elif colored_button.isOver(pos):
                    continue
                
                elif exit_button.isOver(pos):
                    running = False
                
            elif event.type == pygame.MOUSEMOTION:
                if start_button.isOver(pos):
                    start_button.color = OVER

                elif exit_button.isOver(pos):
                    exit_button.color = OVER

                elif colored_button.isOver(pos):
                    colored_button.color = OVER

                else:
                    start_button.color = WHITE
                    colored_button.color = WHITE
                    exit_button.color = WHITE

            elif event.type == pygame.QUIT:
                running = False

        start_button.draw(window, True)
        colored_button.draw(window, True)
        exit_button.draw(window, True)
        pygame.display.flip()
    pygame.quit()

if not pygame.image.get_extended():
    print("Error")
    sys.exit()

pygame.init()

WHITE = (255, 255, 255)
OVER = (225, 209, 65)
GREY = (50, 50, 50)
BLACK = (0, 0, 0)

window_size = (1152, 864)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Interface test")

font = pygame.freetype.Font('upheavtt.ttf', 16)
bg_text = font.render("PIXEL PASSION", BLACK, None, 0, 0, 110)
fg_text = font.render("PIXEL PASSION", WHITE, None, 0, 0, 110)
img_menu = pygame.image.load('bg_menu.png')
window.blits(blit_sequence=((img_menu, (0, 0)), (bg_text[0], ((window_size[0] - bg_text[1].width) // 2, (window_size[1] // 8) + 5)), (fg_text[0], ((window_size[0] - fg_text[1].width) // 2, window_size[1] // 8))))

button_size = (200, 60)
start_button = Button(WHITE, (window_size[0]//2) - button_size[0]//2, (window_size[1]//2) - button_size[1]//2 - 60, button_size[0], button_size[1], "B / W")
colored_button = Button(WHITE, (window_size[0]//2) - button_size[0]//2, (window_size[1]//2) - button_size[1]//2 + 60, button_size[0], button_size[1], "COLORS")
exit_button = Button(WHITE, (window_size[0]//2) - button_size[0]//2, (window_size[1]//2) - button_size[1]//2 + 180, button_size[0], button_size[1], "EXIT")
main_menu()