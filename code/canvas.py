import pixel
import random
import queue
import os
import easygui

class Canvas:
    # Holds a 2d list of pixel objects
    def __init__(self, x, y, width, length):
        self.x = x
        self.y = y
        self.width = width
        self.length = length
        self.width_of_pixel = 5
        self.grid = []
        self.backups = []
        self.active_color = (0, 0, 0)
        self.active_tool = "brush"
        self.current_pixel = []
        self.brush_size = 1
        self.status = ""
        self.current_file = ""
        self.create_grid()
    
    def create_grid(self):
        # Creates a 2d list of pixels objects
        starting_y = self.y
        x = self.x
        for i in range(self.width):
            new_column = []
            for j in range(self.length):
                if starting_y > (self.length - 1) * self.width_of_pixel + self.y:
                    starting_y = self.y
                    x += self.width_of_pixel
                new_column.append(pixel.Pixel((x, starting_y), self.width_of_pixel, self.width_of_pixel, (255, 255, 255)))
                starting_y += self.width_of_pixel
                # if starting_x > (self.width-1)*self.width_of_pixel + self.x:
                #     starting_x = self.x
                #     y += self.width_of_pixel
                # new_column.append(Pixel((starting_x, y), self.width_of_pixel, self.width_of_pixel, (255, 255, 255)))
                # starting_x += self.width_of_pixel
            self.grid.append(new_column)
        
    def add_backup(self): 
        # Saves the current pixel colors (Can Undo no more than 25 times back)

        if len(self.backups) > 25:
            self.backups.pop(0)

        all_colors = []
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                all_colors.append(self.grid[i][j].color)

        if len(self.backups) >= 1:
            if all_colors == self.backups[-1]:
                return 0

        self.backups.append(list(all_colors))
    
    def undo(self):
        # Resets the pixels colors to whatever is last stored in the backup
        if len(self.backups) < 1:
            return 0

        index = 0
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                self.grid[i][j].color = self.backups[-1][index]
                index += 1
        
        self.backups.pop(-1)
    
    def undo_button(self):
        self.undo()
        self.undo()
    
    def color_point(self, i, j, eraser=False):
        if eraser:
            color = (255, 255, 255)
        else:
            color = self.active_color
        
        self.color_with_size(i, j, color)
        if len(self.current_pixel) < 1:
            self.current_pixel = [i, j]
        elif self.brush_size == 0:
            pass
        else:
            pixel_to_color = [i, j]
            while pixel_to_color != self.current_pixel:
                if pixel_to_color[0] > self.current_pixel[0]:
                    pixel_to_color[0] -= 1
                elif pixel_to_color[0] < self.current_pixel[0]:
                    pixel_to_color[0] += 1
                if pixel_to_color[1] > self.current_pixel[1]:
                    pixel_to_color[1] -= 1
                elif pixel_to_color[1] < self.current_pixel[1]:
                    pixel_to_color[1] += 1
                
                self.color_with_size(pixel_to_color[0], pixel_to_color[1], color)
            self.current_pixel = [i, j]

        self.status = ""
    
    def color_with_size(self, x, y, color):
        self.grid[x][y].color = color
        brush_points = 1
        while brush_points < self.brush_size:
            if x - brush_points >= 0:
                self.grid[x - brush_points][y].color = color
            if x + brush_points < self.width:
                self.grid[x + brush_points][y].color = color
            if y - brush_points >= 0:
                self.grid[x][y - brush_points].color = color
            if y + brush_points < self.length:
                self.grid[x][y + brush_points].color = color
                
            brush_points += 1

        if self.brush_size >= 3:
            to_color = self.get_neighbors(x, y, top = False, bottom = False, right = False, left = False)
            for i in to_color:
                self.grid[i[0]][i[1]].color = color
            # self.grid[x + 1][y + 1].color = color
            # self.grid[x + 1][y - 1].color = color
            # self.grid[x - 1][y + 1].color = color
            # self.grid[x - 1][y - 1].color = color

        if self.brush_size >= 4:
            if self.validate_pixel(x + 1, y + 2):
                self.grid[x + 1][y + 2].color = color
            if self.validate_pixel(x + 2, y + 1):
                self.grid[x + 2][y + 1].color = color

            if self.validate_pixel(x + 1, y - 2):
                self.grid[x + 1][y - 2].color = color
            if self.validate_pixel(x + 2, y - 1):
                self.grid[x + 2][y - 1].color = color

            if self.validate_pixel(x - 2, y + 1):
                self.grid[x - 2][y + 1].color = color
            if self.validate_pixel(x - 1, y + 2):
                self.grid[x - 1][y + 2].color = color

            if self.validate_pixel(x - 1, y - 2):
                self.grid[x - 1][y - 2].color = color
            if self.validate_pixel(x - 2, y - 1):
                self.grid[x - 2][y - 1].color = color
        
        if self.brush_size == 5:
            self.color_single_pixel(x + 1, y + 3, color)
            self.color_single_pixel(x + 1, y + 4, color)
            self.color_single_pixel(x + 2, y + 2, color)
            self.color_single_pixel(x + 2, y + 3, color)
            self.color_single_pixel(x + 3, y + 1, color)
            self.color_single_pixel(x + 3, y + 2, color)
            self.color_single_pixel(x + 4, y + 1, color)

            self.color_single_pixel(x - 1, y + 3, color)
            self.color_single_pixel(x - 1, y + 4, color)
            self.color_single_pixel(x - 2, y + 2, color)
            self.color_single_pixel(x - 2, y + 3, color)
            self.color_single_pixel(x - 3, y + 1, color)
            self.color_single_pixel(x - 3, y + 2, color)
            self.color_single_pixel(x - 4, y + 1, color)

            self.color_single_pixel(x + 1, y - 3, color)
            self.color_single_pixel(x + 1, y - 4, color)
            self.color_single_pixel(x + 2, y - 2, color)
            self.color_single_pixel(x + 2, y - 3, color)
            self.color_single_pixel(x + 3, y - 1, color)
            self.color_single_pixel(x + 3, y - 2, color)
            self.color_single_pixel(x + 4, y - 1, color)

            self.color_single_pixel(x - 1, y - 3, color)
            self.color_single_pixel(x - 1, y - 4, color)
            self.color_single_pixel(x - 2, y - 2, color)
            self.color_single_pixel(x - 2, y - 3, color)
            self.color_single_pixel(x - 3, y - 1, color)
            self.color_single_pixel(x - 3, y - 2, color)
            self.color_single_pixel(x - 4, y - 1, color)

        
    def get_neighbors(self, x, y, top = True, top_right = True, right = True, bottom_right = True, bottom = True, bottom_left = True, left = True, top_left = True):
        pixels = []
        if y - 1 >= 0:
            if top:
                pixels.append((x, y - 1))
            if top_right and x + 1 < self.width:
                pixels.append((x + 1, y - 1))
            if top_left and x - 1 >= 0:
                pixels.append((x - 1, y - 1))
        
        if y + 1 < self.length:
            if bottom:
                pixels.append((x, y + 1))
            if bottom_right and x + 1 < self.width:
                pixels.append((x + 1, y + 1))
            if bottom_left and x - 1 >= 0:
                pixels.append((x - 1, y + 1))

        if right and x + 1 < self.width:
            pixels.append((x + 1, y))
        if left and x - 1 >= 0:
            pixels.append((x - 1, y))

        return pixels

    def validate_pixel(self, x, y):
        if x >= 0 and x < self.width and y >= 0 and y < self.length:
            return True
        else:
            return False

    def color_single_pixel(self, x, y, color):
        if self.validate_pixel(x, y):
            self.grid[x][y].color = color
        
    def draw(self, display):
        # Draws each pixel
        for i in self.grid:
            for j in i:
                j.draw_pixel(display)
    
    def change_color(self, amount):
        red = self.active_color[0]
        green = self.active_color[1] 
        blue = self.active_color[2]
        red += amount
        green += amount
        blue += amount

        if red <= 255 and red >= 0 and green <= 255 and green >= 0 and blue <= 255 and blue >= 0:
            self.active_color = (red, green, blue)
    
    def change_to_picker(self):
        self.active_tool = "picker"
    def change_to_fill(self):
        self.active_tool = "fill"
    def change_to_brush(self):
        self.active_tool = "brush"
    def change_to_eraser(self):
        self.active_tool = "eraser"
    
    def flood_fill(self, x, y, new_color):
        old_color = self.grid[x][y].color
        if old_color == new_color:
            return 0
        
        color_queue = queue.Queue()
        color_queue.put((x, y))
        while not color_queue.empty():
            x, y = color_queue.get()
            if x < 0 or x >= self.width or y < 0 or y >= self.length or self.grid[x][y].color != old_color:
                continue
            else:
                self.grid[x][y].color = new_color
                color_queue.put((x+1, y))
                color_queue.put((x-1, y))
                color_queue.put((x, y+1))
                color_queue.put((x, y-1))

    def clear_board(self):
        for i in self.grid:
            for j in i:
                j.color = (255, 255, 255)
    
    def random_fill(self):
        for i in self.grid:
            for j in i:
                red = random.randint(0, 255)
                green = random.randint(0, 255)
                blue = random.randint(0, 255)
                j.color = (red, green, blue)

    def sepia(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                red, green, blue = self.grid[i][j].color[0], self.grid[i][j].color[1], self.grid[i][j].color[2] 
                new_red = int((red * .393) + (green *.769) + (blue * .189))
                new_green = int((red * .349) + (green *.686) + (blue * .168))
                new_blue = int((red * .272) + (green *.534) + (blue * .131))
                if new_red > 255:
                    new_red = 255
                if new_green > 255:
                    new_green = 255
                if new_blue > 255:
                    new_blue = 255
                self.grid[i][j].color = (new_red, new_green, new_blue)
    

    # runs for each pixel adding a greyscale effect
    def greyscale(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                red, green, blue = self.grid[i][j].color[0], self.grid[i][j].color[1], self.grid[i][j].color[2]
                grey = (red * 0.3 + green * 0.59 + blue * 0.11)
                self.grid[i][j].color = (grey, grey, grey)

    def save_picture_as(self):
        if os.path.isdir('../Saves') != True:
            os.mkdir("../Saves")
        
        file_name = easygui.enterbox("NAME OF FILE ", "Save")
        # filename = 'first_save.txt'
        if file_name:
            filename = "../Saves/" + file_name
            if filename[-4:] != ".txt":
                filename += ".txt"

            self.current_file = filename
            if os.path.isfile(filename):
                overwrite = easygui.ynbox("This file already exists, overwrite?", "Overwrite")
                if overwrite == False:
                    self.status = "Did not save"
                    return 1
            f = open(filename, "w+")

            for i in range(len(self.grid)):
                for j in range(len(self.grid[i])):
                    f.write(f"({self.grid[i][j].color[0]},{self.grid[i][j].color[1]},{self.grid[i][j].color[2]})")
            
            f.close()

            self.status = "Saved"
        else:
            self.status = "Could not Save"
    
    def save_picture(self):
        if self.current_file != "":
            f = open(self.current_file, "w+")

            for i in range(len(self.grid)):
                for j in range(len(self.grid[i])):
                    f.write(f"({self.grid[i][j].color[0]},{self.grid[i][j].color[1]},{self.grid[i][j].color[2]})")
            
            f.close()

            self.status = "Saved"
        else:
            self.save_picture_as()

    def load_picture(self):
        file_name = easygui.enterbox("NAME OF FILE ", "Load")
        if file_name:
            filename = "../Saves/" + file_name
            if filename[-4:] != ".txt":
                filename += ".txt"

            self.current_file = filename

            all_colors = []

            try:
                f = open(filename, "r")
                for line in f:
                    colors = line.split(')')
                    for color in colors:
                        color = color.split(',')
                        if color == ['']:
                            break
                        all_colors.append((int(color[0][1:]), int(color[1]), int(color[2])))

                index = 0
                for i in range(len(self.grid)):
                    for j in range(len(self.grid[i])):
                        self.grid[i][j].color = all_colors[index]
                        index += 1

                f.close()
                self.status = "Loaded"
            except:
                self.status = "File not found"
        else:
            self.status = "File Not Found"

