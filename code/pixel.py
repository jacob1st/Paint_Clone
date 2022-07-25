import pygame

class Pixel:
    # A pixel object that has position, color, and size
    def __init__(self, pos, width, height, color):
        self.pos = pos
        self.color = color
        self.width = width
        self.height = height
        self.rectangle = pygame.Rect(pos[0], pos[1], width, height)

    def draw_pixel(self, display):
        # Draws a rectangle
        pygame.draw.rect(display, self.color, self.rectangle)