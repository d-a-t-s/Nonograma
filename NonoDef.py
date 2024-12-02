import pygame
import pygame.freetype
import createBoard
import Constraints
from MenuEsc import menuEsc
from MenuWin import win
from math import *

from NonogramSolver import *

class SurfaceVConstraintCell():

    def __init__(self, surface_v_constraints, cell_size, x, y, font, number):
        self.cell_size = cell_size
        self.font = font
        self.cell = None
        self.x = x
        self.y = y
        self.color = (0,0,135)
        self.character = number
        self.height = self.cell_size if cell_size <= 50 else 50
        self.cell = surface_v_constraints.subsurface(((self.cell_size * self.x, self.height * self.y), (self.cell_size, self.height)))
        self.update(number)
        
    def update(self, character = None):
        desired_height = self.height - 2
        self.cell.fill(self.color, (1 ,1 ,self.cell_size - 2, self.cell_size - 2))
        if character != None:
            self.character = character
            self.cell.fill(self.color, (1 ,1 ,self.cell_size - 2, self.height - 2))
            rect_character = self.font.get_rect("%s" % character,0,0,(self.height)-2)
            if rect_character.width >= self.height:
                height = floor((desired_height / rect_character.width) * desired_height)
                rect_character = self.font.get_rect(None, 0, 0, height)
                self.font.render_to(self.cell, ((self.cell_size - rect_character.width) / 2, (self.height - rect_character.height) / 2), None, (255, 255, 255), None, 0, 0, height)
            else:
                self.font.render_to(self.cell, ((self.cell_size - rect_character.width) / 2, (self.height - rect_character.height) / 2), None, (255, 255, 255), None, 0, 0, desired_height)

class SurfaceVConstraint():

    def __init__(self, cell_size, n_cols, max_constraints_cols, v_constraints, font):
        self.cell_size = cell_size
        self.n_cols = n_cols
        self.n_rows = max_constraints_cols
        self.height = self.cell_size if cell_size <= 50 else 50

        self.cell_matrix = [[0 for i in range(n_cols)] for i in range(self.n_rows)]
        self.surface = pygame.Surface((cell_size * n_cols, self.height * self.n_rows), pygame.SRCALPHA)
        #self.surface.fill((0,0,20,50))

        for x in range(self.n_cols):
            aux = len(v_constraints[x])
            for y in range(self.n_rows):
                if y < self.n_rows - aux:
                    continue
                cell = SurfaceVConstraintCell(self.surface, cell_size, x, y, font, v_constraints[x][aux + y - self.n_rows])
                self.cell_matrix[y][x] = cell
    
    def get_surface(self):
        return self.surface
    
class SurfaceHConstraintCell():

    def __init__(self, surface_h_constraints, cell_size, x, y, font, number):
        self.cell_size = cell_size
        self.font = font
        self.cell = None
        self.x = x
        self.y = y
        self.color = (0,0,135)
        self.character = number
        self.width = self.cell_size if cell_size <= 50 else 50
        self.cell = surface_h_constraints.subsurface(((self.width * self.x, self.cell_size * self.y), (self.width, self.cell_size)))
        self.update()
        
    def update(self):
        desired_height = self.width - 2
        self.cell.fill(self.color, (1 ,1 ,self.cell_size - 2, self.cell_size - 2))
        if self.character != None:
            self.cell.fill(self.color, (1 ,1 ,self.width - 2, self.cell_size - 2))
            rect_character = self.font.get_rect("%s" % self.character,0,0,(self.width)-2)
            if rect_character.width >= self.width:
                height = floor((desired_height / rect_character.width) * desired_height)
                rect_character = self.font.get_rect(None, 0, 0, height)
                self.font.render_to(self.cell, ((self.width - rect_character.width) / 2, (self.cell_size - rect_character.height) / 2), None, (255, 255, 255), None, 0, 0, height)
            else:
                self.font.render_to(self.cell, ((self.width - rect_character.width) / 2, (self.cell_size - rect_character.height) / 2), None, (255, 255, 255), None, 0, 0, desired_height)

class SurfaceHConstraint():

    def __init__(self, cell_size, max_constraints_rows, n_rows, h_constraints, font):
        self.cell_size = cell_size
        self.n_cols = max_constraints_rows
        self.n_rows = n_rows
        self.width = self.cell_size if cell_size <= 50 else 50

        self.cell_matrix = [[0 for i in range(self.n_cols)] for i in range(self.n_rows)]
        self.surface = pygame.Surface((self.width * self.n_cols, self.cell_size * self.n_rows), pygame.SRCALPHA) # * 2
        #self.surface.fill((0,0,20,50))

        for y in range(self.n_rows):
            aux = len(h_constraints[y])
            for x in range(self.n_cols):
                if x < self.n_cols - aux:
                    continue
                cell = SurfaceHConstraintCell(self.surface, self.cell_size, x, y, font, h_constraints[y][aux + x - self.n_cols])
                self.cell_matrix[y][x] = cell
    
    def get_surface(self):
        return self.surface

class SurfaceGridCell():

    def __init__(self, surface_grid, states_board, states, cell_size, x, y, font):
        self.states_board = states_board
        self.states = states
        self.cell_size = cell_size
        self.font = font
        self.cell = None
        self.x = x
        self.y = y
        self.color = None
        self.character = None
        self.cell = surface_grid.subsurface(((self.cell_size*self.x, self.cell_size*self.y),(self.cell_size, self.cell_size)))
        self.height = self.cell_size
        self.update()

    def update(self):
        self.color, self.character = self.states[self.states_board[self.y][self.x]]
        self.cell.fill(self.color, (1 ,1 ,self.cell_size - 2, self.cell_size - 2))
        desired_height = self.height - 2
        if self.character != None:
            self.cell.fill(self.color, (1 , 1, self.cell_size - 2, self.height - 2))
            rect_character = self.font.get_rect("%s" % self.character,0,0,(self.height)-2)
            if rect_character.width >= rect_character.height:
                height = (desired_height / rect_character.width) * desired_height
                rect_character = self.font.get_rect(None, 0, 0, height)
                self.font.render_to(self.cell, ((self.cell.get_width() - rect_character.width + 1) / 2, (self.height - rect_character.height + 1) / 2), None, (255, 0, 0), None, 0, 0, height)
            else:
                self.font.render_to(self.cell, ((self.cell.get_width() - rect_character.width + 1) / 2, (self.height - rect_character.height + 1) / 2), None, (255, 0, 0), None, 0, 0, self.cell.get_width())

class SurfaceGrid():

    def __init__(self, states_board, states ,cell_size, n_cols, n_rows, font):
        self.cell_size = cell_size
        self.n_cols = n_cols
        self.n_rows = n_rows
        self.states_board = states_board
        self.states = states

        self.cell_matrix = [[0 for i in range(n_cols)] for i in range(n_rows)]
        self.surface = pygame.Surface((cell_size * n_cols, cell_size * n_rows), pygame.SRCALPHA)
        self.surface.fill((0,0,200,50))

        for x in range(n_cols):
            for y in range(n_rows):
                cell = SurfaceGridCell(self.surface, self.states_board, self.states, cell_size, x, y, font)
                self.cell_matrix[y][x] = cell

    def update(self, col, row):
        self.cell_matrix[row][col].update()
    
    def get_surface(self):
        return self.surface

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
    pygame.init()
    window_size = (1152, 864)

    cell_size = 50

    zoom = 1
    zoom_min = 0.1
    zoom_max = 3
    zoom_step = 0.03

    font = pygame.freetype.Font('upheavtt.ttf', 16)

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

    clock = pygame.time.Clock()

    running = True
    refresh = True
    solved = False

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
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

            elif event.type == pygame.QUIT:
                running = False

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
            window.blit(img, (0, 0))
            window.blit(grid_render, (offset_x, offset_y))
            window.blit(img, (min(cell_size * zoom, 50) * max_constraints_rows, 0), ((min(cell_size * zoom, 50) * max_constraints_rows, 0),(window_size[0], min(cell_size * zoom, 50) * max_constraints_cols)))
            window.blit(img, (0, min(cell_size * zoom, 50) * max_constraints_cols), ((0, min(cell_size * zoom, 50) * max_constraints_cols),((min(cell_size * zoom, 50) * max_constraints_rows), window_size[1])))
            window.blit(surface_v_constraints, (offset_x, max(0, offset_y - min(cell_size * zoom, 50) * max_constraints_cols)))
            window.blit(surface_h_constraints, (max(0, offset_x - min(cell_size * zoom, 50) * max_constraints_rows), offset_y))
            window.blit(img,(0,0),((0,0),(max(offset_x,min(cell_size * zoom, 50) * max_constraints_rows), max(offset_y,min(cell_size * zoom, 50) * max_constraints_cols))))
            
            pygame.display.flip()
        