from mlx import Mlx
import time
#from schlang import draw_schlang as schlang
from DrawMaze import Maze

class Window():

    def __init__(self, output=None):
        self.mlx = Mlx()
        self.ptr = self.mlx.mlx_init()

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

        self.maze = Maze(self.mlx, self.ptr, self.window)

        self.mlx.mlx_hook(self.window, 33, 0, self.close, None)
        self.mlx.mlx_hook(self.window, 4, 1 << 2, self.mouse_click, None)
        self.mlx.mlx_key_hook(self.window, self.key_event, None)

    def key_event(self, key, param):
        if key == 65307:  #bash xav do sprawdzenia
            self.close(None)
        #if key == 65362:
            #self.window.des

        #print(key)
    


    def button(self):
        self.btn_ptr = self.mlx.mlx_new_image(self.ptr, 100, 100)
        self.mlx_btn_data = self.mlx.mlx_get_data_addr(self.btn_ptr)
        self.btn_data = self.mlx_btn_data[0]
        img_array = self.mlx.mlx_png_file_to_image(self.ptr, "image.png")

        print(img_array[1])
        print(img_array[2])
        self.btn_data[0:4 * 100 * 100] = 100 * 100 * bytes([0, 255, 255, 255])

        #print(img_data[0])
        #print(img_data[2])
        img_data = self.mlx.mlx_get_data_addr(img_array[0])
        self.color_data = img_data[0]
        self.color_lenth = img_data[2]
        #print(list(img_data[0][248:320]))

        #img_data[0][0:4] = bytes([0, 255, 255, 255])

        self.mlx.mlx_put_image_to_window(self.ptr, self.window, img_array[0], 1600, 800)

    def mouse_click(self, button, x, y, param):
        print(f"Mouse on {x} and {y} address. Clicked {button}")
        if ((x >= 1600 and x < 1834) or (y >= 800 and y < 999)): #baisicly window width i window height + img width i img height
            pixelx = x - 1600
            pixely = y - 800
            print(list(self.color_data[pixely * self.color_lenth +  4 * pixelx: pixely * self.color_lenth +  4 * (pixelx + 1)]))
            color = list(self.color_data[pixely * self.color_lenth +  4 * pixelx: pixely * self.color_lenth +  4 * (pixelx + 1)])

            if color != bytes([255, 255, 255, 255]):
                self.maze.i = 0
                self.maze.z = 0
                self.color = color


    def close(self, param):
        self.mlx.mlx_destroy_window(self.ptr, self.window)
        self.mlx.mlx_loop_exit(self.ptr) #zamyka okno

    def show(self):
        self.maze.draw_maze()
        self.button()
        #self.mlx.mlx_loop_hook(self.ptr, self.draw_pixel, None)
        self.mlx.mlx_loop_hook(self.ptr, self.maze.draw_borders, self.color)
        #self.mlx.mlx_loop_hook(self.ptr, schlang(self.mlx, self.window, self.ptr), self)
        self.mlx.mlx_loop(self.ptr)


if __name__ == "__main__":
    window = Window("output2.txt")
    window.show()
