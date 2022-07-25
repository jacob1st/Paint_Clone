import pygame

class Button:
    def __init__(self, x, y, width, height, color, text, on_press):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.do_on_press = on_press
        self.selected = False
        self.hitbox = pygame.Rect(x, y, width, height)

    def draw(self, display):
        if self.selected:
            red, green, blue = self.color[0], self.color[1], self.color[2]
            red -= 35
            green -= 35
            blue -= 35
            if red < 0:
                red = 0
            if green < 0:
                green = 0
            if blue < 0:
                blue = 0
            pygame.draw.rect(display, self.color, self.hitbox, 5)
            pygame.draw.rect(display, (red, green, blue), self.hitbox)
        else:
            pygame.draw.rect(display, self.color, self.hitbox)
        text_font = pygame.font.SysFont("Arial", 16)
        label = text_font.render(self.text, 1, (255, 255, 255))
        display.blit(label, (self.x + int(self.width*.03), self.y + int(self.height*.03)))
    
    def on_press(self):
        self.do_on_press()