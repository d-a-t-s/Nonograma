import pygame
import pygame.freetype
import createBoard
import Constraints
from MenuEsc import menuEsc
from MenuWin import win
from math import *

from NonogramSolver import *

def draw_board(surface, colored_board, cell_size, zoom, offset_x, offset_y, font):
    for row in range(len(colored_board)):
        for col in range(len(colored_board[row])):
            if colored_board[row][col] == 2:
                color = (255, 255, 255)

                rect = pygame.draw.rect(surface, color, ((col * cell_size * zoom + 1) + offset_x, (row * cell_size * zoom + 1) + offset_y, cell_size * zoom - 2, cell_size * zoom - 2))
                x = font.get_rect("X", 0, 0, rect.height)
                height = floor((rect.height / x.width) * rect.height)
                x = font.get_rect("X", 0, 0, floor((rect.height / x.width) * rect.height))

                font.render_to(surface, (rect.x + (rect.width - x.width) / 2, rect.y + (rect.height - x.height) / 2), None, (150, 0, 0), None, 0, 0, height)

            elif colored_board[row][col] == 1:
                color = (0, 0, 0)
                pygame.draw.rect(surface, color, ((col * cell_size * zoom + 1) + offset_x, (row * cell_size * zoom + 1) + offset_y, cell_size * zoom - 2, cell_size * zoom - 2))

            elif colored_board[row][col] == 0:
                color = (255, 255, 255)
                pygame.draw.rect(surface, color, ((col * cell_size * zoom + 1) + offset_x, (row * cell_size * zoom + 1) + offset_y, cell_size * zoom - 2, cell_size * zoom - 2))


def draw_borders(surface, constraints, col_cells, row_cells, grid_size, cell_size, font, zoom, offset_x, offset_y, img):
    zoom_num = 1 if zoom > 1 else zoom
    col = 0
    row = 0
    aux_offset_x = offset_x if offset_x >= cell_size * row_cells * zoom_num else min(cell_size * row_cells * zoom, cell_size * row_cells)
    aux_offset_y = offset_y if offset_y >= cell_size * col_cells * zoom_num else min(cell_size * col_cells * zoom, cell_size * col_cells)

    col_banner = pygame.Rect(0, 0, max(0, min(surface.get_width(), offset_x + grid_size * cell_size * zoom)), min(surface.get_height(), aux_offset_y))
    row_banner = pygame.Rect(0, 0, min(surface.get_width(), aux_offset_x), max(0, min(surface.get_height(), offset_y + grid_size * cell_size * zoom)))
    col_panel = surface.subsurface(col_banner)
    row_panel = surface.subsurface(row_banner)

    col_panel.blit(img, (0, 0))
    row_panel.blit(img, (0, 0))

    for i in constraints[0]:
        aux = col_cells
        for j in i[::-1]:
            aux -= 1
            test = pygame.Rect((offset_x + col * cell_size * zoom + 1, (aux_offset_y - cell_size * zoom_num * (col_cells - aux)), cell_size * zoom - 2, cell_size * zoom_num))
            pygame.draw.rect(surface,(0,0,135), test)
            test2 = font.get_rect("%s" % j,0,0,(cell_size) * zoom_num)
            if test2.width > cell_size * zoom_num:
                font.render_to(surface, (test.x + (test.width - ((cell_size - 2) * zoom_num)) // 2, test.y + ((test.height - floor(((cell_size - 2) * zoom_num / test2.width) * (cell_size - 2) * zoom_num)) // 2)), None, (255, 255, 255), None, 0, 0, floor(((cell_size - 2) * zoom_num / test2.width) * (cell_size - 2) * zoom_num))
            else:
                font.render_to(surface, (test.x + (test.width - test2.width) // 2, test.y + ((test.height - test2.height) // 2)), None, (255, 255, 255), None, 0, 0, cell_size * zoom_num)
        col +=1

    for i in constraints[1]:
        aux = row_cells
        for j in i[::-1]:
            aux -= 1
            test4 = pygame.Rect((aux_offset_x - cell_size * zoom_num * (row_cells - aux)), offset_y + row * cell_size * zoom + 1,  cell_size * zoom_num, cell_size * zoom - 2)
            pygame.draw.rect(surface,(0,0,135), test4)
            test5 = font.get_rect("%s" % j,0,0,cell_size * zoom_num)
            if test5.width > cell_size * zoom_num:
                font.render_to(surface, (test4.x + (test4.width - ((cell_size - 2) * zoom_num)) // 2, test4.y + ((test4.height - floor(((cell_size - 2) * zoom_num / test2.width) * (cell_size - 2) * zoom_num)) // 2)), None, (255, 255, 255), None, 0, 0, floor(((cell_size - 2) * zoom_num / test5.width) * (cell_size - 2) * zoom_num))
            else:
                font.render_to(surface, (test4.x + ((test4.width - test5.width) // 2), test4.y + ((test4.height - test5.height) // 2)), None, (255, 255, 255), None, 0, 0, cell_size * zoom_num)
        row +=1

    aux_banner = pygame.Rect(0, 0, min(surface.get_width(), aux_offset_x), min(surface.get_height(), aux_offset_y))
    aux_panel = surface.subsurface(aux_banner)
    aux_panel.blit(img, (0, 0))

    
          
def handle_click(pos, type, board, Colored_board, cell_size, zoom, offset_x, offset_y):
    row = (floor((pos[1] - offset_y) / (cell_size * zoom)))
    col = (floor((pos[0] - offset_x) / (cell_size * zoom)))
    if 0 <= row < len(board) and 0 <= col < len(board[row]):
        if type == 1:
            board[row][col] = not board[row][col]
            if Colored_board[row][col] != 1:
                Colored_board[row][col] = 1
            else:
                Colored_board[row][col] = 0
        elif type == 3:
            board[row][col] = False
            if Colored_board[row][col] != 2:
                Colored_board[row][col] = 2
            else:
                Colored_board[row][col] = 0

def max_number_contraints(constraints):
    max_constraints_cols = 0
    max_constraints_rows = 0
    for i in constraints[0]:
        max_constraints_cols = max(len(i),max_constraints_cols)
    for i in constraints[1]:
        max_constraints_rows = max(len(i),max_constraints_rows)

    return max_constraints_cols, max_constraints_rows

def check(board, solution_board):
    for i in range(len(solution_board)):
        for j in range(len(solution_board[0])):
            if ((not solution_board[i][j]) and board[i][j]):
                return False
    return True


def game(window, window_size, font, clock, grid_size):
    cell_size = 50
    zoom = 1
    zoom_min = 0.1
    zoom_max = 3
    zoom_step = 0.01

    solved = False
    dragging = False
    panel = pygame.Surface(window_size)
    img = pygame.image.load('bg_nonogram.png')
    panel.blit(img, (0, 0))
    colored_board = [[0 for i in range(grid_size)] for i in range(grid_size)]
    board = [[False for i in range(grid_size)] for i in range(grid_size)]

    solutionBoard = createBoard.createBoard(grid_size)
    constraints = Constraints.constraints(solutionBoard)

    nonogram = Nonogram(constraints[0],constraints[1])
    while not nonogram.solve():
        solutionBoard = createBoard.createBoard(grid_size)
        constraints = Constraints.constraints(solutionBoard)
        nonogram = Nonogram(constraints[0],constraints[1])
    max_constraints_cols, max_constraints_rows = max_number_contraints(constraints)
    offset_x = max(cell_size * max_constraints_rows, (window_size[0] - cell_size * grid_size) // 2)
    offset_y = max(cell_size * max_constraints_cols, (window_size[1] - cell_size * grid_size) // 2)

    check_panel = pygame.Surface((window_size[0] // 4, window_size[1] // 16), pygame.SRCALPHA)
    text_wrong = font.render("There is something wrong...", (255, 255 ,255), None, 0, 0, 20)
    text_correct = font.render("Everything is fine!!", (255, 255 ,255), None, 0 ,0, 20)

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 2: #boton central
                    dragging = True
                    last_mouse_pos = event.pos
                    panel.blit(img, (0, 0))
                    
                elif event.button == 3 and not solved:
                    handle_click(event.pos, 3, board, colored_board, cell_size, zoom, offset_x, offset_y)#3 para boton derecho cambiar por algo legible
                    
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    mouse_x, mouse_y = event.pos
                    offset_x += mouse_x - last_mouse_pos[0]
                    offset_y += mouse_y - last_mouse_pos[1]
                    last_mouse_pos = event.pos
                    panel.blit(img, (0, 0))

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and not solved:
                    handle_click(event.pos, 1, board, colored_board, cell_size, zoom, offset_x, offset_y)#1 para boton izquierdo cambiar por algo legible
                    if board == solutionBoard:
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
                    if not check(board, solutionBoard):
                        check_panel.fill((0, 0, 0, 0))
                        check_panel.blit(text_wrong[0], ((check_panel.get_width() // 2) - text_wrong[1].width // 2, check_panel.get_height() // 2 - text_wrong[1].height // 2))
                        pygame.draw.rect(panel, (0, 0, 0), (window_size[0] - check_panel.get_width() - 5, window_size[1] - check_panel.get_height() * 1.5, window_size[0] // 4, window_size[1] // 16), 0, 5)
                        panel.blit(check_panel, (window_size[0] - check_panel.get_width() - 5, window_size[1] - check_panel.get_height() * 1.5))
                    else:
                        check_panel.fill((0, 0, 0, 0))
                        check_panel.blit(text_correct[0], ((check_panel.get_width() // 2) - text_correct[1].width // 2, check_panel.get_height() // 2 - text_correct[1].height // 2))
                        pygame.draw.rect(panel, (0, 0, 0), (window_size[0] - check_panel.get_width() - 5, window_size[1] - check_panel.get_height() * 1.5, window_size[0] // 4, window_size[1] // 16), 0, 5)
                        panel.blit(check_panel, (window_size[0] - check_panel.get_width() - 5, window_size[1] - check_panel.get_height() * 1.5))

        draw_board(panel, colored_board, cell_size, zoom, offset_x, offset_y, font)
        draw_borders(panel, constraints, max_constraints_cols, max_constraints_rows, grid_size, cell_size, font, zoom, offset_x, offset_y, img)

        window.blit(panel, (0, 0))
        pygame.display.flip()