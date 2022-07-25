import pygame

class Slider:
    def __init__(self, x, y, width, scale = 1, tick = 1):
        self.x = x
        self.y = y
        self.width = width
        self.scale = int(scale)
        self.tick = int(tick)

        self.button = pygame.Rect(x, y - 5, 10, 30)
        self.place_slider(0)
    
    def draw(self, display):
        pygame.draw.rect(display, (0, 0, 0), pygame.Rect(self.x, self.y, self.width * self.scale, 20))
        pygame.draw.rect(display, (255, 255, 255), self.button)

    def slide(self):
        mouse_pos = pygame.mouse.get_pos()
        current_placement = self.button.x
        if mouse_pos[0] > self.x and mouse_pos[0] < self.x + (self.width*self.scale):
            self.button.x = mouse_pos[0]
        elif mouse_pos[0] < self.x:
            self.button.x = self.x
        elif mouse_pos[0] > self.x + (self.width*self.scale):
            self.button.x = self.x + (self.width*self.scale)

        return self.button.x - current_placement
    
    def place_slider(self, pos):
        if pos > self.width:
            self.button.x = self.width * self.scale
        else:
            self.button.x = self.x + (pos*self.scale)
        # if self.x + pos < self.x + self.width:
        #     self.button.x = self.x + pos
        # else:
        #     self.button.x = self.x + self.width

    def read_value(self):
        distance = self.button.x - self.x
        value = int(distance / self.scale)
        value *= self.tick

        return value