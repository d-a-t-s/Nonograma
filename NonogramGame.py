import pygame

def draw_board(surface, board, cell_size):
    for row in range(len(board)):
        for col in range(len(board[row])):
            color = (255, 255, 255)
            pygame.draw.rect(surface, color, (
                (col * cell_size + 1), (row * cell_size + 1), cell_size - 2, cell_size - 2))
            

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

    window.fill((247, 225, 99))
    draw_board(window, board, cell_size)
    pygame.display.flip()
pygame.quit()
