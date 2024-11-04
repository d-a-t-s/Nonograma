import pygame

class Button():

    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text


    def draw(self, surface, outline=None):
        if outline:
            pygame.draw.rect(surface, (0, 0, 0), (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0, 5)

        pygame.draw.rect(surface, (self.color), (self.x, self.y, self.width, self.height), 0, 4)

        if self.text != '':
            font = pygame.font.Font('upheavtt.ttf', self.width//4)
            text = font.render(self.text, True, (0, 0, 0))
            surface.blit(text, (self.x + (self.width / 2 - text.get_width() / 2) + 2, self.y + (self.height / 2 - text.get_height() / 2)))


    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        else:
            return False