import pygame
import pygame.freetype
from MenuEsc import menuEsc
from MenuWin import win
from math import *
from BaseButton import Button

from ColorNonoBoard import *
from NonogramSolver import *

def draw_board(surface, colored_board, cell_size, zoom, offset_x, offset_y, palette):
    for row in range(len(colored_board)):
        for col in range(len(colored_board[row])):
            pygame.draw.rect(surface, palette[colored_board[row][col]], ((col * cell_size * zoom + 1) + offset_x, (row * cell_size * zoom + 1) + offset_y, cell_size * zoom - 2, cell_size * zoom - 2))


def draw_borders(surface, col_constraint, row_constraint,max_c_cols, max_c_rows, grid_cols, grid_rows, cell_size, font, zoom, offset_x, offset_y, palette , img):
    zoom_num = 1 if zoom > 1 else zoom
    col = 0
    row = 0
    aux_offset_x = offset_x if offset_x >= cell_size * max_c_rows * zoom_num else min(cell_size * max_c_rows * zoom, cell_size * max_c_rows)
    aux_offset_y = offset_y if offset_y >= cell_size * max_c_cols * zoom_num else min(cell_size * max_c_cols * zoom, cell_size * max_c_cols)

    col_banner = pygame.Rect(0, 0, max(0, min(surface.get_width(), offset_x + grid_cols * cell_size * zoom)), min(surface.get_height(), aux_offset_y))
    row_banner = pygame.Rect(0, 0, min(surface.get_width(), aux_offset_x), max(0, min(surface.get_height(), offset_y + grid_rows * cell_size * zoom)))
    col_panel = surface.subsurface(col_banner)
    row_panel = surface.subsurface(row_banner)

    col_panel.blit(img, (0, 0))
    row_panel.blit(img, (0, 0))

    for i in col_constraint:
        aux = max_c_cols
        for j in i[::-1]:
            aux -= 1
            test = pygame.Rect((offset_x + col * cell_size * zoom + 1, (aux_offset_y - cell_size * zoom_num * (max_c_cols - aux)), cell_size * zoom - 2, cell_size * zoom_num))
            pygame.draw.rect(surface,palette[j[1]], test)
            test2 = font.get_rect("%s" % j[0],0,0,(cell_size) * zoom_num)
            if test2.width > cell_size * zoom_num:
                font.render_to(surface, (test.x + (test.width - ((cell_size - 2) * zoom_num)) // 2, test.y + ((test.height - floor(((cell_size - 2) * zoom_num / test2.width) * (cell_size - 2) * zoom_num)) // 2)), None, (255, 255, 255), None, 0, 0, floor(((cell_size - 2) * zoom_num / test2.width) * (cell_size - 2) * zoom_num))
            else:
                font.render_to(surface, (test.x + (test.width - test2.width) // 2, test.y + ((test.height - test2.height) // 2)), None, (255, 255, 255), None, 0, 0, cell_size * zoom_num)
        col +=1

    for i in row_constraint:
        aux = max_c_rows
        for j in i[::-1]:
            aux -= 1
            test4 = pygame.Rect((aux_offset_x - cell_size * zoom_num * (max_c_rows - aux)), offset_y + row * cell_size * zoom + 1,  cell_size * zoom_num, cell_size * zoom - 2)
            pygame.draw.rect(surface,palette[j[1]], test4)
            test5 = font.get_rect("%s" % j[0],0,0,cell_size * zoom_num)
            if test5.width > cell_size * zoom_num:
                font.render_to(surface, (test4.x + (test4.width - ((cell_size - 2) * zoom_num)) // 2, test4.y + ((test4.height - floor(((cell_size - 2) * zoom_num / test5.width) * (cell_size - 2) * zoom_num)) // 2)), None, (255, 255, 255), None, 0, 0, floor(((cell_size - 2) * zoom_num / test5.width) * (cell_size - 2) * zoom_num))
            else:
                font.render_to(surface, (test4.x + ((test4.width - test5.width) // 2), test4.y + ((test4.height - test5.height) // 2)), None, (255, 255, 255), None, 0, 0, cell_size * zoom_num)
        row +=1

    aux_banner = pygame.Rect(0, 0, min(surface.get_width(), aux_offset_x), min(surface.get_height(), aux_offset_y))
    aux_panel = surface.subsurface(aux_banner)
    aux_panel.blit(img, (0, 0))

    
          
def handle_click(pos, color, Colored_board, cell_size, zoom, offset_x, offset_y):
    row = (floor((pos[1] - offset_y) / (cell_size * zoom)))
    col = (floor((pos[0] - offset_x) / (cell_size * zoom)))
    if 0 <= row < len(Colored_board) and 0 <= col < len(Colored_board[row]):
        Colored_board[row][col] = color

def max_number_contraints(col_constraint, row_constraint):
    max_constraints_cols = 0
    max_constraints_rows = 0
    for i in col_constraint:
        max_constraints_cols = max(len(i),max_constraints_cols)
    for i in row_constraint:
        max_constraints_rows = max(len(i),max_constraints_rows)

    return max_constraints_cols, max_constraints_rows

def check(board_solved, colored_board,palette):
    x = len(palette)-1
    for i in range(len(board_solved)):
        for j in range(len(board_solved[0])):
            if ((board_solved[i][j] != colored_board[i][j])) and (colored_board[i][j] != x):
                return False
    return True

def color_selection(window_size, palette):
    button_size = window_size[1] // 16
    buttons = []
    for i in range(len(palette)):
        buttons.append(Button(palette[i], (window_size[1] // 24) * (i+1) + button_size * (i), (window_size[1] - window_size[1] // 8) + button_size - button_size // 2, button_size, button_size))

    return buttons


def game(window, window_size, font, clock):
    cell_size = 20
    zoom = 1
    zoom_min = 0.1
    zoom_max = 3
    zoom_step = 0.01
    selected_color = 5
    board_solved = []
    palette = []

    solved = False
    dragging = False
    panel = pygame.Surface(window_size)
    img = pygame.image.load('bg_nonogram.png')
    panel.blit(img, (0, 0))

    palette, col_constraint, row_constraint, board_solved = board_colored_nono()

    grid_cols = len(col_constraint)
    grid_rows = len(row_constraint)
    palette.append((255,255,255))
    colored_board = [[len(palette) - 1 for i in range(grid_cols)] for i in range(grid_rows)]

    buttons = color_selection(window_size, palette)
    #panel_buttons = pygame.Surface((window_size[0], window_size[1] // 8))
    #window.blit(panel, (0, window_size[1] - window_size[1] // 8))

    max_constraints_cols, max_constraints_rows = max_number_contraints(col_constraint, row_constraint)
    offset_x = max(cell_size * max_constraints_rows, (window_size[0] - cell_size * grid_cols) // 2)
    offset_y = max(cell_size * max_constraints_cols, (window_size[1] - cell_size * grid_rows) // 2)

    check_panel = pygame.Surface((window_size[0] // 4, window_size[1] // 16), pygame.SRCALPHA)
    text_wrong = font.render("There is something wrong...", (255, 255 ,255), None, 0, 0, 20)
    text_correct = font.render("Everything is fine!!", (255, 255 ,255), None, 0 ,0, 20)

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i in buttons:
                        if i.isOver(pos):
                            selected_color = palette.index(i.color)

                if event.button == 2: #boton central
                    dragging = True
                    last_mouse_pos = event.pos
                    panel.blit(img, (0, 0))
                    
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    mouse_x, mouse_y = event.pos
                    offset_x += mouse_x - last_mouse_pos[0]
                    offset_y += mouse_y - last_mouse_pos[1]
                    last_mouse_pos = event.pos
                    panel.blit(img, (0, 0))

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and not solved:
                    handle_click(event.pos, selected_color, colored_board, cell_size, zoom, offset_x, offset_y)#1 para boton izquierdo cambiar por algo legible
                    if colored_board == board_solved:
                        solved = True
                        quited = win(window, window_size, font, clock)
                    else:
                        solved = False
                        quited = False

                    if quited:
                        running = False
                
                if event.button == 2:  # Boton central
                    dragging = False

            elif event.type == pygame.MOUSEWHEEL: #al parecer button 4 y 5 son el scroll !!!cambiar importante crash inminente
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if event.y > 0:
                    zoom_new = min(zoom_max, zoom + zoom_step)

                elif event.y < 0:
                    zoom_new = max(zoom_min, zoom - zoom_step)
                offset_x = mouse_x - (mouse_x - offset_x) * (zoom_new / zoom)
                offset_y = mouse_y - (mouse_y - offset_y) * (zoom_new / zoom)

                zoom = zoom_new
                panel.blit(img, (0, 0))
            
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    if solved:
                        quited = win(window, window_size, font, clock)
                    else:
                        quited = menuEsc(window, window_size[0], window_size[1], font, clock)

                    if quited:
                        running = False
                elif event.key == pygame.K_SPACE:
                    panel.blit(img, (0, 0))
                    
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not check(board_solved, colored_board,palette):
                        check_panel.fill((0, 0, 0, 0))
                        check_panel.blit(text_wrong[0], ((check_panel.get_width() // 2) - text_wrong[1].width // 2, check_panel.get_height() // 2 - text_wrong[1].height // 2))
                        pygame.draw.rect(panel, (0, 0, 0), (window_size[0] - check_panel.get_width() - 5, window_size[1] - check_panel.get_height() * 1.5, window_size[0] // 4, window_size[1] // 16), 0, 5)
                        panel.blit(check_panel, (window_size[0] - check_panel.get_width() - 5, window_size[1] - check_panel.get_height() * 1.5))
                    else:
                        check_panel.fill((0, 0, 0, 0))
                        check_panel.blit(text_correct[0], ((check_panel.get_width() // 2) - text_correct[1].width // 2, check_panel.get_height() // 2 - text_correct[1].height // 2))
                        pygame.draw.rect(panel, (0, 0, 0), (window_size[0] - check_panel.get_width() - 5, window_size[1] - check_panel.get_height() * 1.5, window_size[0] // 4, window_size[1] // 16), 0, 5)
                        panel.blit(check_panel, (window_size[0] - check_panel.get_width() - 5, window_size[1] - check_panel.get_height() * 1.5))

                    
        #panel.blit(panel_buttons, (0, window_size[1] - window_size[1] // 8))
        draw_board(panel, colored_board, cell_size, zoom, offset_x, offset_y, palette)
        draw_borders(panel, col_constraint, row_constraint, max_constraints_cols, max_constraints_rows, grid_cols, grid_rows, cell_size, font, zoom, offset_x, offset_y,palette ,img)
        for i in buttons:
            i.draw(panel, True)
        window.blit(panel, (0, 0))
        pygame.display.flip()