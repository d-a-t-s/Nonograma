import pygame, pygame.freetype
from NonoDefTest import game

def main_menu():
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    game()
                    pygame.display.set_mode(window_size)
            if event.type == pygame.QUIT:
                running = False
        
        window.fill(GREY)
        menu_font.render_to(window, ((window_size[0]//2) - (window_size[0]//5), (window_size[1]//2) - (window_size[1]//8)), "Press SPACE to play", WHITE)

        pygame.display.flip()
    pygame.quit()


pygame.init()

WHITE = (255, 255, 255)
GREY = (50, 50, 50)

window_size = (800, 600)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Interface test")
menu_font = pygame.freetype.SysFont('Arial', 40)

main_menu()