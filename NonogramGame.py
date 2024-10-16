import pygame

def draw_board(surface, board, cell_size):
    for row in range(len(board)):
        for col in range(len(board[row])):
            color = (255, 255, 255)
            if board[row][col]:
                color = (0, 0, 0)
            pygame.draw.rect(surface, color, (
                cell_size + (col * cell_size + 1), cell_size + (row * cell_size + 1), cell_size - 2, cell_size - 2))

def draw_borders(surface, grid_size, cell_size):
	pygame.draw.rect(surface, (100,0,0), (cell_size, 0, grid_size * cell_size, cell_size))
	pygame.draw.rect(surface, (100,0,0), (0, cell_size, cell_size, grid_size * cell_size))

def handle_click(pos, board, cell_size):
    row = (pos[1] // cell_size) -1
    col = (pos[0] // cell_size) -1
    if 0 <= row < len(board) and 0 <= col < len(board[row]):
        board[row][col] = not board[row][col]            

pygame.init()
grid_size = 10
cell_size = 50
window_size = grid_size * cell_size
window = pygame.display.set_mode((window_size, window_size))
clock = pygame.time.Clock()
board = [[False for i in range(grid_size)] for i in range(grid_size)]

running = True
while running:
    clock.tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            handle_click(event.pos, board, cell_size)

    window.fill((247, 225, 99))
    draw_borders(window, grid_size, cell_size)
    draw_board(window, board, cell_size)
    pygame.display.flip()
pygame.quit()
