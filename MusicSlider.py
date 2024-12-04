import pygame

class Slider():
    
    def __init__(self, handle_color, track_color, x, y, width, height, min, max, val):
        self.handle_color = handle_color
        self.track_color = track_color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min = min
        self.max = max
        self.val = val
        self.radius = height // 2
        self.slider_x = self.x + (self.val - self.min) / (self.max - self.min) * self.width
        self.dragging = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.track_color, (self.x, self.y + self.height // 2 - 2, self.width, 4))
        pygame.draw.circle(surface, self.handle_color, (int(self.slider_x), self.y + self.height // 2), self.radius)

    def isOver(self, pos):
        if pos[0] > self.slider_x - self.radius and pos[0] < self.slider_x + self.radius:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.isOver(event.pos):
                self.dragging = True
            elif self.x <= event.pos[0] <= self.x + self.width and self.y <= event.pos[1] <= self.y + self.height:
                self.slider_x = event.pos[0]
                self.update_value()

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.slider_x = max(self.x, min(event.pos[0], self.x + self.width))
                self.update_value()

    def update_value(self):
        self.val = self.min + (self.slider_x - self.x) / self.width * (self.max - self.min)
        pygame.mixer.music.set_volume(self.val)

    def get_value(self):
        return self.val