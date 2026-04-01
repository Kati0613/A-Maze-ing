from mlx import Mlx
import time
#from schlang import draw_schlang as schlang
from DrawMaze import Maze
from Image import Image
from Button import Button

class Window():

    def __init__(self, output=None):
        self.mlx = Mlx()
        self.ptr = self.mlx.mlx_init()
        self.holy = {1485: False, 1482: False, 50: False}

        validator, width, height = self.mlx.mlx_get_screen_size(self.ptr)
        self.color = bytes([255, 255, 255, 255])

        if validator != 0:
            print("Błąd przy pobieraniu rozmiaru ekranu")

        print(width)
        print(height)

        self.window = self.mlx.mlx_new_window(
            self.ptr, width, height, "whoores"
            )

        self.output = output
        self.path_show = False

        self.maze = Maze(self.mlx, self.ptr, self.window, output)

        self.mlx.mlx_hook(self.window, 33, 0, self.close, None)
        self.mlx.mlx_hook(self.window, 4, 1 << 2, self.mouse_click, None)
        self.mlx.mlx_key_hook(self.window, self.key_event, None)
        self.papa = True

    def key_event(self, key, param):
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
            print(self.papei.show)
            self.papei.show_button()
        elif key == 65363:
            size = self.button2.update_int(1)
            if self.maze.size != size:
                self.maze.size = size
                self.redraw()
        elif key == 65361:
            size = self.button2.update_int(-1)
            if self.maze.size != size:
                self.maze.size = size
                self.redraw()
        elif key == 65293:
            pass
        print(key)

    def mouse_click(self, button, x, y, param):
        print(f"Mouse on {x} and {y} address. Clicked {button}")
        if ((x >= 1600 and x < 1834) and (y >= 700 and y < 899)): #baisicly window width i window height + img width i img height
            pixelx = x - 1600
            pixely = y - 700
            color = self.button.color_data[pixely * self.button.size_line +  4 * pixelx: pixely * self.button.size_line +  4 * (pixelx + 1)]
            #print(list(color))

            if button == 1:
                if self.color != color and color != bytes([0, 0, 0, 0]):
                    self.color = color
                    self.redraw()
                    print("COLOR:", list(color))
            elif button == 3:
                if color != bytes([0, 0, 0, 0]):
                    self.maze.draw_fourtytwo(color)
                    self.papei.show = False
    
    def redraw(self):
        self.mlx.mlx_clear_window(self.ptr, self.window)
        self.maze.draw_maze(self.color)
        self.button.show_button()
        self.mouse_left.show_button()
        self.mouse_right.show_button()
        self.p_key.show_button()
        self.button2.refresh()
        self.papei.show = False
        self.mlx.mlx_string_put(self.ptr, self.window, 1600, 920, 0xFFFFFF, "Change size:")
        self.regenerate.show_button()

    def close(self, param):
        self.mlx.mlx_destroy_window(self.ptr, self.window)
        self.mlx.mlx_loop_exit(self.ptr) #zamyka okno


    def show(self):
        self.button = Image(self.ptr, self.window, self.mlx, 1600, 700)
        self.papei = Image(self.ptr, self.window, self.mlx, 200, 720, "4837205_print_1.png", False)
        self.mouse_left = Image(self.ptr, self.window, self.mlx, 1640, 558, "mouse.png")
        self.mouse_right = Image(self.ptr, self.window, self.mlx, 1730, 570, "42colormouse.png")
        self.button2 = Button(self.ptr, self.window, self.mlx, 1630, 950, 70, 20, self.maze.size)
        self.regenerate = Image(self.ptr, self.window, self.mlx, 1740, 920, "enter.png", )
        self.mlx.mlx_string_put(self.ptr, self.window, 1600, 920, 0xFFFFFF, "Change size:")
        self.p_key = Image(self.ptr, self.window, self.mlx, 1680, 460, "keyboard_key_p.png")
        self.maze.draw_maze()
        self.button.show_button()
        self.mouse_left.show_button()
        self.p_key.show_button()
        self.mouse_right.show_button()
        self.regenerate.show_button()
        self.mlx.mlx_loop(self.ptr)



if __name__ == "__main__":
    window = Window("output_test.txt")
    window.show()
