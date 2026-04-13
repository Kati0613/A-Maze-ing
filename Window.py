from mlx import Mlx
import time
from DrawMaze import Maze
from Image import Image
from Button import Button
from typing import List, Union, Set, Generator, Optional, Tuple
from MazeGenerator import MazeGenerator
from Maze import Maze as Maze2

class Window():

    def __init__(self, output=None, maze_width = 10, maze_height = 10, entry = (0, 0), exit = (10, 10)):
        self.mlx = Mlx()
        self.ptr = self.mlx.mlx_init()
        self.holy = {1485: False, 1482: False, 50: False}

        validator, width, height = self.mlx.mlx_get_screen_size(self.ptr)
        self.color = bytes([255, 255, 255, 255])

        if validator != 0:
            print("Błąd przy pobieraniu rozmiaru ekranu")

        self.window = self.mlx.mlx_new_window(
            self.ptr, width, height, "whoores"
            )

        self.output = output
        self.path_show = False

        self.entry = entry
        self.exit = exit

        self.maze = Maze(self.mlx, self.ptr, self.window, output, maze_width, maze_height, entry, exit)

        self.mlx.mlx_hook(self.window, 33, 0, self.close, None)
        self.mlx.mlx_hook(self.window, 4, 1 << 2, self.mouse_click, None)
        self.mlx.mlx_key_hook(self.window, self.key_event, None)
        self.papa = True

    def key_event(self, key, param):
        #print(key)
        if key == 65307:  #bash xav do sprawdzenia
            self.close(None)
        elif key == 112:
            if not self.path_show:
                self.path_show = True
                self.maze.draw_path(bytes([0, 255, 255, 255]))
            else:
                self.path_show = False
                self.maze.draw_path(bytes([0, 0, 0, 255]))
                self.button()
        elif key == 106:
            self.papei.show = not self.papei.show
            self.papei.show_button()
        elif key == 65363:
            self.button_width.update_int(1, 150, 10)
        elif key == 65361:
            self.button_width.update_int(-1, 150, 10)
        elif key == 65293:
            self.maze.clear_image()
            if (int(self.button_width.word) == self.maze.width and int(self.button_height.word) == self.maze.height):
                maze = Maze2(self.maze.width, self.maze.height, self.maze.entry, self.maze.exit, False)
            else:
                self.maze.width = int(self.button_width.word)
                self.maze.height = int(self.button_height.word)
                maze = Maze2(self.maze.width, self.maze.height, (0, 0), (self.maze.width - 1, self.maze.height - 1), False)#jak to zrobic skad wziac parametry entry i exit bez parametow            
                self.maze.entry = (0, 0)
                self.maze.exit = (self.maze.width - 1, self.maze.height - 1)
                self.maze.update_size()
                self.button_size.word = str(self.maze.size)
                self.button_size.put_str()
            self.maze.output = maze_gen.cerate_maze(maze)
            self.redraw()
        elif key == 65362:
            self.button_height.update_int(1, 150, 10)
        elif key == 65364:
            self.button_height.update_int(-1, 150, 10)
        #print(key)


    def mouse_click(self, button, x, y, param):
        if button == 4:
            size = self.button_size.update_int(1, self.maze.max)
            if self.maze.size != size:
                self.maze.size = size
                self.redraw()
        if button == 5:
            size = self.button_size.update_int(-1, self.maze.max)
            if self.maze.size != size:
                self.maze.size = size
                self.redraw()
        #print(button)
        if ((x >= 1600 and x < 1834) and (y >= 630 and y < 829)): #baisicly window width i window height + img width i img height
            pixelx = x - 1600
            pixely = y - 630
            color = self.button.color_data[pixely * self.button.size_line +  4 * pixelx: pixely * self.button.size_line +  4 * (pixelx + 1)]
            #print(list(color))
            if button == 1:
                if self.color != color and color != bytes([0, 0, 0, 0]):
                    self.color = color
                    self.redraw()
                    #print("COLOR:", list(color))
            elif button == 3:
                if color != bytes([0, 0, 0, 0]):
                    self.maze.draw_fourtytwo(color)
                    self.maze.put_maze_to_window()
    
    def redraw(self):
        self.maze.clear_image()
        self.maze.draw_maze(self.color)


    def close(self, param):
        self.mlx.mlx_destroy_window(self.ptr, self.window)
        self.mlx.mlx_loop_exit(self.ptr)#zamyka okno

    def show(self):
        self.button = Image(self.ptr, self.window, self.mlx, 1600, 630)
        self.papei = Image(self.ptr, self.window, self.mlx, 170, 720, "4837205_print_1.png", False)
        self.mouse_left = Image(self.ptr, self.window, self.mlx, 1640, 488, "mouse.png")
        self.mouse_right = Image(self.ptr, self.window, self.mlx, 1730, 500, "42colormouse.png")
        self.regenerate = Image(self.ptr, self.window, self.mlx, 1730, 919, "enter.png")
        self.mlx.mlx_string_put(self.ptr, self.window, 1650, 845, 0xFFFFFF, "Scale:")
        self.p_key = Image(self.ptr, self.window, self.mlx, 1680, 390, "keyboard_key_p.png")
        self.button_size = Button(self.ptr, self.window, self.mlx, 1720, 845, 70, 20, self.maze.size)
        self.mlx.mlx_string_put(self.ptr, self.window, 1610, 931, 0xFFFFFF, "Height:")
        self.up_key = Image(self.ptr, self.window, self.mlx, 1686, 891, "keyboard_key_up.png", True)
        self.down_key = Image(self.ptr, self.window, self.mlx, 1686, 971, "keyboard_key_down.png", True)
        self.button_height = Button(self.ptr, self.window, self.mlx, 1686, 916, 20, 50, self.maze.height)
        self.mlx.mlx_string_put(self.ptr, self.window, 1520, 931, 0xFFFFFF, "Width:")
        self.button_width = Button(self.ptr, self.window, self.mlx, 1523, 956, 50, 20, self.maze.width)
        self.left_key = Image(self.ptr, self.window, self.mlx, 1500, 956, "keyboard_key_left.png", True)
        self.right_key = Image(self.ptr, self.window, self.mlx, 1576, 956, "keyboard_key_right.png", True)

        self.up_key.show_button()
        self.down_key.show_button()
        self.button.show_button()
        self.maze.draw_maze(bytes([255, 255, 255, 255]))
        self.right_key.show_button()
        self.left_key.show_button()
        self.mouse_left.show_button()
        self.p_key.show_button()
        self.mouse_right.show_button()
        self.regenerate.show_button()
        self.mlx.mlx_loop(self.ptr)

if __name__ == "__main__":
    maze_gen = MazeGenerator()
    maze = Maze2(10, 10, (0, 0) , (4, 2), False)
    output = maze_gen.cerate_maze(maze, 1)
    window = Window(output, maze.width, maze.height, maze.entry, maze.exit)
    window.show()
