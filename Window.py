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
        self.color = bytes([0, 255, 255, 255])

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
            


        print(key)

    def mouse_click(self, button, x, y, param):
        print(f"Mouse on {x} and {y} address. Clicked {button}")
        if ((x >= 1600 and x < 1834) and (y >= 700 and y < 899)): #baisicly window width i window height + img width i img height
            pixelx = x - 1600
            pixely = y - 700
            color = self.button.color_data[pixely * self.button.size_line +  4 * pixelx: pixely * self.button.size_line +  4 * (pixelx + 1)]

            if button == 1:
                if self.color != color and color != bytes([0, 0, 0, 0]):
                    #self.maze.i = 0
                    #self.maze.z = 0
                    self.color = color
                    self.redraw()
                    print("COLOR:", list(color))
                    print("Click")
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
        self.papei.show = False

    def close(self, param):
        self.mlx.mlx_destroy_window(self.ptr, self.window)
        self.mlx.mlx_loop_exit(self.ptr) #zamyka okno


    def show(self):
        self.button = Image(self.ptr, self.window, self.mlx, 1600, 700)
        self.papei = Image(self.ptr, self.window, self.mlx, 200, 720, "4837205_print_1.png", False)
        self.mouse_left = Image(self.ptr, self.window, self.mlx, 1640, 558, "mouse.png")
        self.mouse_right = Image(self.ptr, self.window, self.mlx, 1730, 570, "42colormouse.png")
        self.button2 = Button(self.ptr, self.window, self.mlx, 1650, 960, 70, 20, "22")
        self.button3 = Button(self.ptr, self.window, self.mlx, 1760, 935, 20, 70, "1")
        #self.mlx.mlx_string_put(self.ptr, self.window, 1600, 960, 0xFFFFFF, str(self.maze.width_img))
        #self.mlx.mlx_string_put(self.ptr, self.window, 1550, 960, 0xFFFFFF, str(self.maze.height_img))
        napis = "Click P to show"
        self.p_key = Image(self.ptr, self.window, self.mlx, 1680, 460, "keyboard_key_p.png")
        self.maze.draw_maze()
        self.button.show_button()
        self.mouse_left.show_button()
        self.p_key.show_button()
        self.mouse_right.show_button()
        
        
        
        #self.maze.draw_path()
        #self.mlx.mlx_loop_hook(self.ptr, self.maze.draw_borders, self.color)
        self.mlx.mlx_loop(self.ptr)



if __name__ == "__main__":
    window = Window("output_test.txt")
    window.show()
