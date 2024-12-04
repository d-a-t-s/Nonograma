import pygame
from BaseButton import Button
from MusicSlider import Slider
from Guardar import cargar_matriz
from NonoDef import game as b_w_game
from ColorNono import game as c_game

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

    button_list = []

    rigth_button = Button(WHITE, window_size[0]//3 * 2 - button_size[1], window_size[1] - button_size[1] * 1.5, button_size[1], button_size[1], ">")
    left_button = Button(WHITE, window_size[0]//3, window_size[1] - button_size[1] * 1.5, button_size[1], button_size[1], "<")
    quit_button = Button(WHITE, (window_size[0]//2) - button_size[0]//2, window_size[1] - button_size[1] * 1.5, button_size[0], button_size[1], "GO BACK")

    puzzles = cargar_matriz('matrices.pkl')
    loaded_puzzles = 0
    for i in range(len(puzzles)):

        if i % 6 <= 2:
            button = Button(WHITE, (window_size[0]//2 - window_size[0]//10) + window_size[0]//4 * (i % 3 - 1), window_size[1]//3 - window_size[1]//8, window_size[0]//5, window_size[0]//5, f"{len(puzzles[i][0][0])} x {len(puzzles[i][0])}")
            button_list.append(button)
            loaded_puzzles += 1

        else: 
            button = Button(WHITE, (window_size[0]//2 - window_size[0]//10) + window_size[0]//4 * (i % 3 - 1), window_size[1]//3 + window_size[1]//5, window_size[0]//5, window_size[0]//5, f"{len(puzzles[i][0][0])} x {len(puzzles[i][0])}")
            button_list.append(button)
            loaded_puzzles += 1

    page = 0
    running = True
    while running:
        clock.tick(60)
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                for i in range(6 * page, min(6 * (page + 1), len(puzzles))):
                    if button_list[i].isOver(pos):
                        if puzzles[i][2][2][1] == "x":
                            b_w_game(window, window_size, font, clock, len(puzzles[i][0][0]), len(puzzles[i][0]), puzzles[i][0], puzzles[i][1], puzzles[i][2])

                        else:
                            c_game(window, window_size, font, clock, puzzles[i][0], puzzles[i][1], puzzles[i][2])

                        running = False

                if rigth_button.isOver(pos) and len(puzzles)//6 > page:
                    page += 1
                    panel.blits(blit_sequence=((img, (0, 0)), (bg_text[0], ((window_size[0] - bg_text[1].width) // 2, 55)), (fg_text[0], ((window_size[0] - fg_text[1].width) // 2, 50))))

                
                elif left_button.isOver(pos) and page > 0:
                    page -= 1
                    panel.blits(blit_sequence=((img, (0, 0)), (bg_text[0], ((window_size[0] - bg_text[1].width) // 2, 55)), (fg_text[0], ((window_size[0] - fg_text[1].width) // 2, 50))))


                elif quit_button.isOver(pos):
                    running = False

            elif event.type == pygame.MOUSEMOTION:
                for button in button_list:
                    if button.isOver(pos):
                        button.color = OVER

                    else:
                        button.color = WHITE

                if rigth_button.isOver(pos):
                    rigth_button.color = OVER

                elif left_button.isOver(pos):
                    left_button.color = OVER

                elif quit_button.isOver(pos):
                    quit_button.color = OVER

                else:
                    rigth_button.color = WHITE
                    left_button.color = WHITE
                    quit_button.color = WHITE


            volume_slider.handle_event(event)
            panel.blit(sub_img, (60, 30))

        volume_slider.val = pygame.mixer.music.get_volume()
        volume_slider.draw(panel)

        for i in range(6 * page, min(6 * (page + 1), len(puzzles))):
            button_list[i].draw(panel, True)

        if len(puzzles)//6 > page:
            rigth_button.draw(panel, True)

        if page > 0:
            left_button.draw(panel, True)

        quit_button.draw(panel, True)
        window.blit(panel, (0, 0))
        pygame.display.flip()