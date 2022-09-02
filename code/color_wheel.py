import pygame
from PIL import Image

class ColorWheel:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        pilImage = Image.open("../images/color_wheel.png")
        self.color_wheel = pygame.image.fromstring(pilImage.tobytes(), pilImage.size, pilImage.mode) 
        self.width = pilImage.size[0]
        self.height = pilImage.size[1]

        self.hitbox = pygame.Rect(x, y, self.width, self.height)
    
    def draw(self, display):
        display.blit(self.color_wheel, (self.x, self.y))
