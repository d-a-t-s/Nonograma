import pygame
import pygame.freetype
import tkinter.filedialog
import Image2

from MenuEsc import menuEsc
from MenuWin import win
from math import *
from BaseButton import Button
from Guardar import guardar_matriz

from ColorNonoBoard import *
from NonogramSolver import *
from SurfaceNonogram import *
          
def handle_click(pos, type, states_board, cell_size, offset_x, offset_y, surface_grid):
    row = (floor((pos[1] - offset_y) / (cell_size)))
    col = (floor((pos[0] - offset_x) / (cell_size)))

    if 0 <= row < len(states_board) and 0 <= col < len(states_board[row]):
        states_board[row][col] = type

        surface_grid.update(col,row)
            
def max_number_contraints(constraints):
    max_constraints = 0
    for i in constraints:
        max_constraints = max(len(i),max_constraints)
    return max_constraints

def check(board_solved, states_board, n_color):
    for i in range(len(board_solved)):
        for j in range(len(board_solved[0])):
            if ((board_solved[i][j] != states_board[i][j]) and (states_board[i][j] != (n_color - 1))):
                return False
    return True

def color_selection(window_size, states):
    button_size = window_size[1] // 16
    buttons = []
    for i in range(len(states)):
        buttons.append(Button(states[i], (window_size[1] // 24) * (i+1) + button_size * (i), (window_size[1] - window_size[1] // 8) + button_size - button_size // 2, button_size, button_size))

    return buttons

def game(window, window_size, font, clock, solutionBoard = None, states_board = None, states_loaded = None):
    cell_size = 50
    zoom = 1
    zoom_min = 0.1
    zoom_max = 3
    zoom_step = 0.03
    selected_color = 2
    board_solved = solutionBoard
    states = states_loaded
    constraints_cols = []
    constraints_rows = []

    solved = False
    dragging = False

    if solutionBoard == None and states_board == None and states_loaded == None:
        user_image = tkinter.filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if not user_image:
            return

        ruta_imagen = user_image
        num_colores = 6   # Número de colores
        nueva_resolucion = (50, 50)  # Nueva resolución deseada (ancho, alto)
        point = ruta_imagen.index('.')
        ruta = ruta_imagen[:point]
        resolution = str(nueva_resolucion[0]) + 'x' + str(nueva_resolucion[1])
        txt = ruta + '_' + resolution
        imagen_simplificada = Image2.simplificar_colores(ruta_imagen, num_colores, nueva_resolucion)

        states, board_solved = Image2.leer_pixeles(imagen_simplificada)
        states.append((255,255,255))


    for i in range(len(board_solved)):
            tempList = []
            aux = None
            counter = 0
            for j in range(len(board_solved[0])):
                if board_solved[i][j] == aux:
                    counter += 1
                elif aux == None:
                    counter += 1
                    aux = board_solved[i][j]
                else:
                    tempList.append((counter, aux))
                    aux = board_solved[i][j]
                    counter = 1
                    continue
            tempList.append((counter, aux))
            constraints_rows.append(tempList)
    for j in range(len(board_solved[0])):
            tempList = []
            aux = None
            counter = 0
            for i in range(len(board_solved)):
                if board_solved[i][j] == aux:
                    counter += 1
                elif aux == None:
                    counter += 1
                    aux = board_solved[i][j]
                else:
                    tempList.append((counter, aux))
                    aux = board_solved[i][j]
                    counter = 1
                    continue
            tempList.append((counter, aux))
            constraints_cols.append(tempList)

    n_cols = len(constraints_cols)
    n_rows = len(constraints_rows)
    if states_board == None:
        states_board = [[len(states) - 1 for i in range(n_cols)] for i in range(n_rows)]

    buttons = color_selection(window_size, states)

    max_constraints_cols = max_number_contraints(constraints_cols)
    max_constraints_rows = max_number_contraints(constraints_rows)

    temp_zoom = window_size[0] / ((n_cols + max_constraints_rows) * cell_size)
    if (temp_zoom < zoom):
        zoom = temp_zoom

    temp_zoom = window_size[1] / ((n_rows + max_constraints_rows) * cell_size)
    if (temp_zoom < zoom):
        zoom = temp_zoom

    if (zoom < zoom_min):
        zoom = zoom_min

    offset_x = max(cell_size * max_constraints_rows * zoom, (window_size[0] - cell_size * n_cols) * zoom // 2)
    offset_y = max(cell_size * max_constraints_cols * zoom, (window_size[1] - cell_size * n_rows) * zoom // 2)

    surface_grid = SurfaceGrid(states_board, states, cell_size * zoom, n_cols, n_rows, font)
    grid_render = surface_grid.get_surface()

    v_constraints = SurfaceVConstraint(cell_size * zoom, n_cols, max_constraints_cols, constraints_cols, font, states)
    surface_v_constraints = v_constraints.get_surface()

    h_constraints = SurfaceHConstraint(cell_size * zoom, max_constraints_rows, n_rows, constraints_rows, font, states)
    surface_h_constraints = h_constraints.get_surface()

    check_panel = pygame.Surface((window_size[0] // 4, window_size[1] // 16), pygame.SRCALPHA)
    text_wrong = font.render("There is something wrong...", (255, 255 ,255), None, 0, 0, 20)
    text_correct = font.render("Everything is fine!!", (255, 255 ,255), None, 0 ,0, 20)
    dragging = False

    img = pygame.image.load('bg_nonogram.png').convert()

    running = True
    refresh = True
    checked = False
    solved = False
    quited = False
    list = [False, False]

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i in buttons:
                        if i.isOver(pos):
                            selected_color = states.index(i.color)

                if event.button == 2: #boton central
                    refresh = True
                    dragging = True
                    last_mouse_pos = event.pos
                    
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    refresh = True
                    mouse_x, mouse_y = event.pos
                    offset_x += mouse_x - last_mouse_pos[0]
                    offset_y += mouse_y - last_mouse_pos[1]
                    last_mouse_pos = event.pos

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and not solved:
                    refresh = True
                    handle_click(event.pos, selected_color, states_board, cell_size * zoom, offset_x, offset_y, surface_grid)#1 para boton izquierdo cambiar por algo legible
                    if states_board == board_solved:
                        solved = True
                        quited = win(window, window_size, font, clock)
                    else:
                        solved = False
                        quited = False
                    if quited:
                        running = False
                
                if event.button == 2:  # Boton central
                    dragging = False

            elif event.type == pygame.MOUSEWHEEL: #button 4 y 5 son el scroll
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
                v_constraints = SurfaceVConstraint(cell_size * zoom, n_cols, max_constraints_cols, constraints_cols, font, states)
                surface_v_constraints = v_constraints.get_surface()
                h_constraints = SurfaceHConstraint(cell_size * zoom, max_constraints_rows, n_rows, constraints_rows, font, states)
                surface_h_constraints = h_constraints.get_surface()
            
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    refresh = True
                    if solved:
                        quited = win(window, window_size, font, clock)
                    else:
                        list = menuEsc(window, window_size[0], window_size[1], font, clock)

                    if quited or list[0]:
                        running = False
                        
                elif event.key == pygame.K_SPACE:
                    checked = False
                    refresh = True
                    
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    checked = True
                    refresh = True

        if list[1]:
            guardar_matriz(board_solved, states_board, states)
            list[1] = False
                    
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
            
            for i in buttons:
                i.draw(window, True)

            if checked:
                if not check(board_solved, states_board, len(states)):
                    check_panel.fill((0, 0, 0, 0))
                    check_panel.blit(text_wrong[0], ((check_panel.get_width() // 2) - text_wrong[1].width // 2, check_panel.get_height() // 2 - text_wrong[1].height // 2))
                    pygame.draw.rect(window, (0, 0, 0), (window_size[0] - check_panel.get_width() - 5, window_size[1] - check_panel.get_height() * 1.5, window_size[0] // 4, window_size[1] // 16), 0, 5)
                    window.blit(check_panel, (window_size[0] - check_panel.get_width() - 5, window_size[1] - check_panel.get_height() * 1.5))
                else:
                    check_panel.fill((0, 0, 0, 0))
                    check_panel.blit(text_correct[0], ((check_panel.get_width() // 2) - text_correct[1].width // 2, check_panel.get_height() // 2 - text_correct[1].height // 2))
                    pygame.draw.rect(window, (0, 0, 0), (window_size[0] - check_panel.get_width() - 5, window_size[1] - check_panel.get_height() * 1.5, window_size[0] // 4, window_size[1] // 16), 0, 5)
                    window.blit(check_panel, (window_size[0] - check_panel.get_width() - 5, window_size[1] - check_panel.get_height() * 1.5))

            pygame.display.flip()