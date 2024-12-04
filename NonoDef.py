import pygame
import pygame.freetype
import createBoard
import Constraints
from MenuEsc import menuEsc
from MenuWin import win

from NonogramSolver import *
from SurfaceNonogram import *

def handle_click(pos, type, states_board, board, n_cols, n_rows, cell_size, offset_x, offset_y, surface_grid):
    row = (floor((pos[1] - offset_y) / (cell_size)))
    col = (floor((pos[0] - offset_x) / (cell_size)))

    if 0 <= row < n_rows and 0 <= col < n_cols:
        if type == 1:
            board[row][col] = not board[row][col]
            if states_board[row][col] != 1:
                states_board[row][col] = 1
            else:
                states_board[row][col] = 0
        elif type == 3:
            board[row][col] = False
            if states_board[row][col] != 2:
                states_board[row][col] = 2
            else:
                states_board[row][col] = 0

        surface_grid.update(col,row)
            
def max_number_contraints(constraints):
    max_constraints = 0
    for i in constraints:
        max_constraints = max(len(i),max_constraints)
    return max_constraints

def check(board, solution_board):
    for i in range(len(solution_board)):
        for j in range(len(solution_board[0])):
            if ((not solution_board[i][j]) and board[i][j]):
                return False
    return True


def game(window, window_size, font, clock, n_cols, n_rows):
    cell_size = 50
    zoom = 1
    zoom_min = 0.1
    zoom_max = 3
    zoom_step = 0.03

    states = [((255,255,255),None),((0,0,0),(None)),((255,255,255),("x"))]

    states_board = [[0 for i in range(n_cols)] for i in range(n_rows)]
    board = [[False for i in range(n_cols)] for i in range(n_rows)]

    ###

    solutionBoard = createBoard.createBoard(n_cols, n_rows)
    constraints_cols, constraints_rows = Constraints.constraints(solutionBoard)

    nonogram = Nonogram(constraints_cols, constraints_rows)
    while not nonogram.solve():
        solutionBoard = createBoard.createBoard(n_cols, n_rows)
        constraints_cols, constraints_rows = Constraints.constraints(solutionBoard)
        nonogram = Nonogram(constraints_cols, constraints_rows)

    max_constraints_cols = max_number_contraints(constraints_cols)
    max_constraints_rows = max_number_contraints(constraints_rows)

    ###
    
    surface_grid = SurfaceGrid(states_board, states, cell_size, n_cols, n_rows, font)
    grid_render = surface_grid.get_surface()

    v_constraints = SurfaceVConstraint(cell_size, n_cols, max_constraints_cols, constraints_cols, font)
    surface_v_constraints = v_constraints.get_surface()

    h_constraints = SurfaceHConstraint(cell_size, max_constraints_rows, n_rows, constraints_rows, font)
    surface_h_constraints = h_constraints.get_surface()


    offset_x = max(cell_size * max_constraints_rows, (window_size[0] - cell_size * n_cols) // 2)
    offset_y = max(cell_size * max_constraints_cols, (window_size[1] - cell_size * n_rows) // 2)

    check_panel = pygame.Surface((window_size[0] // 4, window_size[1] // 16), pygame.SRCALPHA)
    text_wrong = font.render("There is something wrong...", (255, 255 ,255), None, 0, 0, 20)
    text_correct = font.render("Everything is fine!!", (255, 255 ,255), None, 0 ,0, 20)
    dragging = False

    
    img = pygame.image.load('bg_nonogram.png').convert()

    running = True
    refresh = True
    solved = False

    while running:
        clock.tick(60)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 2: #boton central
                    refresh = True
                    dragging = True
                    last_mouse_pos = event.pos
                elif event.button == 3:
                    refresh = True
                    handle_click(event.pos, 3, states_board, board, n_cols, n_rows, cell_size * zoom, offset_x, offset_y, surface_grid)#3 para boton derecho cambiar por algo legible

            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    refresh = True
                    mouse_x, mouse_y = event.pos
                    offset_x += mouse_x - last_mouse_pos[0]
                    offset_y += mouse_y - last_mouse_pos[1]
                    last_mouse_pos = event.pos

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    refresh = True
                    handle_click(event.pos, 1, states_board, board, n_cols, n_rows, cell_size * zoom, offset_x, offset_y, surface_grid)
                    if board == solutionBoard:
                        solved = True
                        quited = win(window, window_size, font, clock)
                    else:
                        solved = False
                        quited = False
                    if quited:
                        running = False

                elif event.button == 2:  # Boton central
                    dragging = False
            
            elif event.type == pygame.MOUSEWHEEL: #al parecer button 4 y 5 son el scroll !!!cambiar importante crash inminente
                refresh = True
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if event.y > 0:
                    zoom_new = min(zoom_max, zoom + zoom_step)

                elif event.y < 0:
                    zoom_new = max(zoom_min, zoom - zoom_step)
                offset_x = mouse_x - (mouse_x - offset_x) * (zoom_new / zoom)
                offset_y = mouse_y - (mouse_y - offset_y) * (zoom_new / zoom)
                zoom = zoom_new

                del surface_grid
                del grid_render

                surface_grid = SurfaceGrid(states_board, states, cell_size * zoom, n_cols, n_rows, font)
                grid_render = surface_grid.get_surface()
                v_constraints = SurfaceVConstraint(cell_size * zoom, n_cols, max_constraints_cols, constraints_cols, font)
                surface_v_constraints = v_constraints.get_surface()
                h_constraints = SurfaceHConstraint(cell_size * zoom, max_constraints_rows, n_rows, constraints_rows, font)
                surface_h_constraints = h_constraints.get_surface()
            
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    refresh = True
                    if solved:
                        quited = win(window, window_size, font, clock)
                    else:
                        quited = menuEsc(window, window_size[0], window_size[1], font, clock)

                    if quited:
                        running = False
                elif event.key == pygame.K_SPACE:
                    window.blit(img, (0, 0))

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not check(board, solutionBoard):
                        check_panel.fill((0, 0, 0, 0))
                        check_panel.blit(text_wrong[0], ((check_panel.get_width() // 2) - text_wrong[1].width // 2, check_panel.get_height() // 2 - text_wrong[1].height // 2))
                        pygame.draw.rect(window, (0, 0, 0), (window_size[0] - check_panel.get_width() - 5, window_size[1] - check_panel.get_height() * 1.5, window_size[0] // 4, window_size[1] // 16), 0, 5)
                        window.blit(check_panel, (window_size[0] - check_panel.get_width() - 5, window_size[1] - check_panel.get_height() * 1.5))
                    else:
                        check_panel.fill((0, 0, 0, 0))
                        check_panel.blit(text_correct[0], ((check_panel.get_width() // 2) - text_correct[1].width // 2, check_panel.get_height() // 2 - text_correct[1].height // 2))
                        pygame.draw.rect(window, (0, 0, 0), (window_size[0] - check_panel.get_width() - 5, window_size[1] - check_panel.get_height() * 1.5, window_size[0] // 4, window_size[1] // 16), 0, 5)
                        window.blit(check_panel, (window_size[0] - check_panel.get_width() - 5, window_size[1] - check_panel.get_height() * 1.5))

        if refresh == True:
            refresh = False
            offset_contraints_x = (offset_x - surface_h_constraints.get_width()) * (surface_h_constraints.get_width() / (grid_render.get_width() + surface_h_constraints.get_width()))
            offset_contraints_y = (offset_y - surface_v_constraints.get_height()) * (surface_v_constraints.get_height() / (grid_render.get_height() + surface_v_constraints.get_height()))
            window.blit(img, (0, 0))
            window.blit(grid_render, (offset_x, offset_y))

            max(offset_y - min(cell_size * zoom, 50) * max_constraints_cols, (offset_y - min(cell_size * zoom, 50) * max_constraints_cols)*(max_constraints_cols)/n_rows)
            
            window.blit(img, (0, 0), ((0, 0),(window_size[0], offset_contraints_y + surface_v_constraints.get_height())))
            window.blit(img, (0, 0), ((0, 0),(offset_contraints_x + surface_h_constraints.get_width(), window_size[1])))
            
            window.blit(surface_v_constraints, (offset_x, max(offset_contraints_y, offset_y - surface_v_constraints.get_height())))
            window.blit(surface_h_constraints, (max(offset_contraints_x, offset_x - surface_h_constraints.get_width()), offset_y))

            window.blit(img,(0,0),((0,0),(max(offset_contraints_x + surface_h_constraints.get_width(), offset_x), max(offset_contraints_y + surface_v_constraints.get_height(), offset_y))))
            pygame.display.flip()