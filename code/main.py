# Clean up brush, add comments, GUI, effects, load, save images, selection
import pygame
from PIL import Image

import button
import canvas
import color_wheel
import slider

def draw_screen():
    # Draw eveything onto the screen
    display.fill((60, 60, 60))
    canvas.draw(display)
    
    color_wheel.draw(display)

    write(f"Darken/Lighten Color", 740, 70)
    darkness_slider.draw(display)

    brush_size_slider.draw(display)

    write(f"TOOLS", 760, 420, size=26, color=(170, 56, 89))
    write(f"----------------------------------------------------", 700, 450)

    write(f"EFFECTS", 200, 10, size=26, color=(170, 56, 89))
    write(f"----------------------------------------------------", 150, 50)

    # Brush size text
    write(f"Brush size: {brush_size_slider.read_value()}", 670, 490)

    # All the button
    for i in buttons:
        i.draw(display)
    
    # Active Color Square
    pygame.draw.rect(display, (255, 255, 255), pygame.Rect(830, 130, 100, 30), 1)
    pygame.draw.rect(display, canvas.active_color, pygame.Rect(835, 135, 90, 20))
    # RGB color
    write(f"Active Color: ({canvas.active_color[0]}, {canvas.active_color[1]}, {canvas.active_color[2]})", 670, 135)

    check_tool()
    
    # Icon of active tool
    mouse_pos = pygame.mouse.get_pos()
    if mouse_pos[0] > canvas.x and mouse_pos[0] < canvas.x + (canvas.width*canvas.width_of_pixel) and mouse_pos[1] > canvas.y and mouse_pos[1] < canvas.y + (canvas.length*canvas.width_of_pixel):
        pygame.mouse.set_visible(False)
        if canvas.active_tool == "picker":
            pygame.draw.circle(display, display.get_at((mouse_pos[0], mouse_pos[1])), (mouse_pos[0], mouse_pos[1]), canvas.brush_size * 5)
            pygame.draw.circle(display, (0, 0, 0), (mouse_pos[0], mouse_pos[1]), canvas.brush_size * 5, 1)
        elif canvas.active_color == (255, 255, 255):
            pygame.draw.circle(display, canvas.active_color, (mouse_pos[0], mouse_pos[1]), canvas.brush_size * 5)
            pygame.draw.circle(display, (0, 0, 0), (mouse_pos[0], mouse_pos[1]), canvas.brush_size * 5, 1)
        else:
            pygame.draw.circle(display, canvas.active_color, (mouse_pos[0], mouse_pos[1]), canvas.brush_size * 5)
            pygame.draw.circle(display, (255, 255, 255), (mouse_pos[0], mouse_pos[1]), canvas.brush_size * 5, 1)

        pilImage = Image.open(f"images/{canvas.active_tool}.png")
        mouse_image = pygame.image.fromstring(pilImage.tobytes(), pilImage.size, pilImage.mode) 
        display.blit(mouse_image, (mouse_pos[0] - 25, mouse_pos[1] - 25))
    else:
        pygame.mouse.set_visible(True)

    pygame.display.update()

def write(msg, x, y, color=(255, 255, 255), font="Arial", size = 12):
    text_font = pygame.font.SysFont(font, size)
    label = text_font.render(msg, 1, color)
    display.blit(label, (x, y))

def check_tool():
    if canvas.active_tool == "brush":
        buttons[0].selected = True
    else:
        buttons[0].selected = False
    if canvas.active_tool == "picker":
        buttons[1].selected = True
    else:
        buttons[1].selected = False
    if canvas.active_tool == "fill":
        buttons[2].selected = True
    else:
        buttons[2].selected = False
    if canvas.active_tool == "eraser":
        buttons[3].selected = True
    else:
        buttons[3].selected = False

# Initialize important pygame variables
pygame.init()
pygame.display.set_caption("Paint")
display = pygame.display.set_mode((1000, 800))
clock = pygame.time.Clock()

# Create a canvas
canvas = canvas.Canvas(10, 155, 128, 128)

darkness_slider = slider.Slider(670, 100, 255)
brush_size_slider = slider.Slider(780, 485, 5, scale=30)

color_wheel = color_wheel.ColorWheel(700, 170)

buttons = [button.Button(670, 550, 100, 20, (58, 150, 247), "Brush", canvas.change_to_brush),
            button.Button(800, 550, 100, 20, (255, 0, 0), "Color Picker", canvas.change_to_picker), 
            button.Button(800, 580, 100, 20, (255, 0, 0), "Fill Tool", canvas.change_to_fill),
            button.Button(670, 580, 100, 20, (255, 0, 0), "Eraser", canvas.change_to_eraser),  
            button.Button(70, 100, 100, 20, (255, 0, 0), "Random", canvas.random_fill), 
            button.Button(200, 100, 100, 20, (255, 0, 0), "Sepia", canvas.sepia), 
            button.Button(330, 100, 100, 20, (255, 0, 0), "Grey scale", canvas.greyscale),
            button.Button(580, 120, 70, 20, (100, 100, 100), "Clear", canvas.clear_board),
            button.Button(470, 120, 70, 20, (100, 100, 100), "Undo", canvas.undo_button)]

def main():
    mouse_pressed = False
    undo = False
    slide_d = False
    slide_b = False

    run = True
    while run:
        clock.tick(120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Closed the window
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN: # If mouse is clicked
                mouse_pos = pygame.mouse.get_pos()
                found_button = False
                canvas.add_backup()
                for i in buttons:
                    if i.hitbox.collidepoint(mouse_pos):
                        i.on_press()
                        found_button = True
                        break

                if color_wheel.hitbox.collidepoint(mouse_pos):
                    canvas.active_color = display.get_at((mouse_pos[0], mouse_pos[1]))
                    darkness_slider.place_slider(int((canvas.active_color[0] + canvas.active_color[1] + canvas.active_color[2])/3))
                elif darkness_slider.button.collidepoint(mouse_pos):
                    slide_d = True
                elif brush_size_slider.button.collidepoint(mouse_pos):
                    slide_b = True
                elif found_button != True:
                    mouse_pressed = True

            
        if mouse_pressed: 
            # Color anywhere the mouse is hovered over while it is pressed
            if pygame.mouse.get_pressed()[0] != True:
                mouse_pressed = False
                canvas.current_pixel = []
            elif canvas.active_tool == "brush":
                for i in range(len(canvas.grid)):
                        for j in range(len(canvas.grid[i])):
                            if canvas.grid[i][j].rectangle.collidepoint(pygame.mouse.get_pos()):
                                canvas.color_point(i, j)
            elif canvas.active_tool == "eraser":
                for i in range(len(canvas.grid)):
                        for j in range(len(canvas.grid[i])):
                            if canvas.grid[i][j].rectangle.collidepoint(pygame.mouse.get_pos()):
                                canvas.color_point(i, j, eraser=True)
            elif canvas.active_tool == "picker":
                for i in canvas.grid:
                    for j in i:
                        if j.rectangle.collidepoint(pygame.mouse.get_pos()):
                            canvas.active_color = j.color
            elif canvas.active_tool == "fill":
                for i in range(len(canvas.grid)):
                    for j in range(len(canvas.grid[i])):
                        if canvas.grid[i][j].rectangle.collidepoint(pygame.mouse.get_pos()) and mouse_pressed:
                            canvas.flood_fill(i, j, canvas.active_color)
                            mouse_pressed = False


        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LCTRL] and keys[pygame.K_z] and undo == False:
            undo = True
            canvas.undo()
        elif keys[pygame.K_z] != True:
            undo = False

        if slide_d:
            if pygame.mouse.get_pressed()[0] != True:
                slide_d = False
            else:
                amount = darkness_slider.slide()
                canvas.change_color(amount)
        
        if slide_b:
            if pygame.mouse.get_pressed()[0] != True:
                slide_b = False
            else:
                brush_size_slider.slide()
                canvas.brush_size = brush_size_slider.read_value()



        draw_screen()


    pygame.quit

main()