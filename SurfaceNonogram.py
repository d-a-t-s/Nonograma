import pygame
import pygame.freetype

from math import floor

class SurfaceVConstraintCell():

    def __init__(self, surface_v_constraints, cell_size, x, y, font, number, color = (0,0,135)):
        self.cell_size = cell_size
        self.font = font
        self.cell = None
        self.x = x
        self.y = y
        self.color = color
        self.character = number
        self.height = self.cell_size if cell_size <= 50 else 50
        self.cell = surface_v_constraints.subsurface(((self.cell_size * self.x, self.height * self.y), (self.cell_size, self.height)))
        self.update(self.color)
        
    def update(self, color = None):
        if (color != None):
            self.color = color
        desired_height = self.height - 2
        self.cell.fill(self.color, (1 ,1 ,self.cell_size - 2, self.cell_size - 2))
        if self.character != None:
            self.cell.fill(self.color, (1 ,1 ,self.cell_size - 2, self.height - 2))
            rect_character = self.font.get_rect("%s" % self.character,0,0,(self.height)-2)
            if rect_character.width >= self.height:
                height = floor((desired_height / rect_character.width) * desired_height)
                rect_character = self.font.get_rect(None, 0, 0, height)
                self.font.render_to(self.cell, ((self.cell_size - rect_character.width) / 2, (self.height - rect_character.height) / 2), None, (255, 255, 255), None, 0, 0, height)
            else:
                self.font.render_to(self.cell, ((self.cell_size - rect_character.width) / 2, (self.height - rect_character.height) / 2), None, (255, 255, 255), None, 0, 0, desired_height)

class SurfaceVConstraint():

    def __init__(self, cell_size, n_cols, max_constraints_cols, v_constraints, font, states = None):
        self.cell_size = cell_size
        self.n_cols = n_cols
        self.n_rows = max_constraints_cols
        self.height = self.cell_size if cell_size <= 50 else 50

        self.cell_matrix = [[0 for i in range(n_cols)] for i in range(self.n_rows)]
        self.surface = pygame.Surface((cell_size * n_cols, self.height * self.n_rows), pygame.SRCALPHA)

        for x in range(self.n_cols):
            aux = len(v_constraints[x])
            for y in range(self.n_rows):
                if y < self.n_rows - aux:
                    continue
                if (states != None):
                    cell = SurfaceVConstraintCell(self.surface, cell_size, x, y, font, v_constraints[x][aux + y - self.n_rows][0], states[v_constraints[x][aux + y - self.n_rows][1]])
                else:
                    cell = SurfaceVConstraintCell(self.surface, cell_size, x, y, font, v_constraints[x][aux + y - self.n_rows])
                self.cell_matrix[y][x] = cell
    
    def get_surface(self):
        return self.surface
    
class SurfaceHConstraintCell():

    def __init__(self, surface_h_constraints, cell_size, x, y, font, number, color = (0,0,135)):
        self.cell_size = cell_size
        self.font = font
        self.cell = None
        self.x = x
        self.y = y
        self.color = color
        self.character = number
        self.width = self.cell_size if cell_size <= 50 else 50
        self.cell = surface_h_constraints.subsurface(((self.width * self.x, self.cell_size * self.y), (self.width, self.cell_size)))
        self.update(self.color)
        
    def update(self, color = None):
        if (color != None):
            self.color = color
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

    def __init__(self, cell_size, max_constraints_rows, n_rows, h_constraints, font, states = None):
        self.cell_size = cell_size
        self.n_cols = max_constraints_rows
        self.n_rows = n_rows
        self.width = self.cell_size if cell_size <= 50 else 50

        self.cell_matrix = [[0 for i in range(self.n_cols)] for i in range(self.n_rows)]
        self.surface = pygame.Surface((self.width * self.n_cols, self.cell_size * self.n_rows), pygame.SRCALPHA)

        for y in range(self.n_rows):
            aux = len(h_constraints[y])
            for x in range(self.n_cols):
                if x < self.n_cols - aux:
                    continue
                if (states != None):
                    cell = SurfaceHConstraintCell(self.surface, cell_size, x, y, font, h_constraints[y][aux + x - self.n_cols][0], states[h_constraints[y][aux + x - self.n_cols][1]])
                else:
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
        if (len(self.states[self.states_board[self.y][self.x]]) == 2):
            self.color, self.character = self.states[self.states_board[self.y][self.x]]
        else:
            self.color = self.states[self.states_board[self.y][self.x]]
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

    def __init__(self, states_board, states, cell_size, n_cols, n_rows, font):
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
    