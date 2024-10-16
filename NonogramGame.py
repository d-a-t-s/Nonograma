import pygame
import pygame.freetype
import createBoard
import Constraints

def draw_board(surface, board, cell_size):
    for row in range(len(board)):
        for col in range(len(board[row])):
            color = (255, 255, 255)
            if board[row][col]:
                color = (0, 0, 0)
            pygame.draw.rect(surface, color, (cell_size + (col * cell_size + 1), cell_size + (row * cell_size + 1), cell_size - 2, cell_size - 2))

def draw_borders(surface, constraints, grid_size, cell_size, font):
	pygame.draw.rect(surface, (100,0,0), (cell_size, 0, grid_size * cell_size, cell_size))
	pygame.draw.rect(surface, (100,0,0), (0, cell_size, cell_size, grid_size * cell_size))
	for i in range(grid_size):
		aux = ' '.join(str(x) for x in constraints[0][i])
		font.render_to(surface, ((cell_size) * (i+1) +10, 5), aux, (255, 255, 255), None, 0, 0, cell_size//len(constraints[0][i]))
		aux = ' '.join(str(x) for x in constraints[1][i])
		font.render_to(surface, (10, (cell_size) * (i+1) +5), aux, (255, 255, 255), None, 0, 0, cell_size//len(constraints[1][i]))
          
def handle_click(pos, board, cell_size):
    row = (pos[1] // cell_size) -1
    col = (pos[0] // cell_size) -1
    if 0 <= row < len(board) and 0 <= col < len(board[row]):
        board[row][col] = not board[row][col]            

pygame.init()
grid_size = 10
cell_size = 50
my_font = pygame.freetype.SysFont('Arial', cell_size //3)
window_size = grid_size * cell_size
window = pygame.display.set_mode((window_size + cell_size, window_size + cell_size))
clock = pygame.time.Clock()
board = [[False for i in range(grid_size)] for i in range(grid_size)]
solutionBoard = createBoard.createBoard(grid_size)
constraints = Constraints.constraints(solutionBoard)

running = True
while running:
    clock.tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            handle_click(event.pos, board, cell_size)

    window.fill((0, 0, 0))
    draw_board(window, board, cell_size)
    draw_borders(window, constraints, grid_size, cell_size, my_font)
    if board == solutionBoard:
        pygame.draw.rect(window, (239, 184, 19), (0, 0, cell_size - 2, cell_size - 2))
        my_font.render_to(window, ((cell_size - (cell_size//4) *2) / 2.5, (cell_size - cell_size//4) //2), "WIN", (0, 0, 0))

    pygame.display.flip()
pygame.quit()
