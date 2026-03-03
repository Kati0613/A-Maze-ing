from mlx import Mlx
import time
from schlang import draw_schlang as schlang


class Window():

    def __init__(self, output = None):
        self.mlx = Mlx()
        self.ptr = self.mlx.mlx_init()
        self.i = 0

        validator, width, height = self.mlx.mlx_get_screen_size(self.ptr)

        if validator != 0:
            print("Błąd przy pobieraniu rozmiaru ekranu")

        print(width)
        print(height)


        self.window = self.mlx.mlx_new_window(
            self.ptr, width, height, "whoores"
            )

        self.output = output

        self.img_ptr = self.mlx.mlx_new_image(self.ptr, 800, 800) # 800 to piksele czyli jeden piksel to 4 bity czyli jeden bajt
        self.mlx_img_data = self.mlx.mlx_get_data_addr(self.img_ptr)
        print(self.mlx_img_data)
        print(self.mlx_img_data)
        self.image_data = self.mlx_img_data[0]
        self.line_length = self.mlx_img_data[2]
        self.image_data[:] = bytes([0,0,0,255]) * (len(self.image_data)//4)
        self.image_data[0:self.line_length] = bytes([255,255,255,255]) * (self.mlx_img_data[2] // 4)
        self.image_data[self.line_length: 2*self.line_length] = bytes([255,255,255,255]) * (self.mlx_img_data[2] // 4)
        self.image_data[2*self.line_length: 3*self.line_length] = bytes([255,255,255,255]) * (self.mlx_img_data[2] // 4)
        self.image_data[20*self.line_length:21*self.line_length] = bytes([255,255,255,255]) * (self.mlx_img_data[2] // 4)
        self.image_data[21*self.line_length:22*self.line_length] = bytes([255,255,255,255]) * (self.mlx_img_data[2] // 4)
        self.image_data[22*self.line_length:23*self.line_length] = bytes([255,255,255,255]) * (self.mlx_img_data[2] // 4)
        #self.image_data[y*self.line_length:23*self.line_length] = bytes([255,255,255,255]) * (self.mlx_img_data[2] // 4)

        self.mlx.mlx_put_image_to_window(self.ptr, self.window, self.img_ptr, 300, 300)
        self.mlx.mlx_hook(self.window, 33, 0, self.close, None)
        self.mlx.mlx_key_hook(self.window, self.key_event, None)

        #schlang(self.mlx, self.window, self.ptr)

    def key_event(self, key, param):
        if key == 65307:  #bash xav do sprawdzenia
            self.close(None)
    
    def draw_window(self, param):
        if self.i < 800:
            self.image_data[27*self.line_length + 4*self.i:27*self.line_length+4*(self.i + 1)] = bytes([255,255,255,255])
            self.image_data[28*self.line_length + 4*self.i:28*self.line_length+4*(self.i + 1)] = bytes([255,255,255,255])
            self.image_data[29*self.line_length + 4*self.i:29*self.line_length+4*(self.i + 1)] = bytes([255,255,255,255])
            #self.image_data[23*self.line_length:23*self.line_length+4*i] = bytes([255,255,255,255])
            self.mlx.mlx_put_image_to_window( self.ptr, self.window, self.img_ptr, 300, 300)
            self.i += 1
    
    def close(self, param):
        self.mlx.mlx_destroy_window(self.ptr, self.window)
        self.mlx.mlx_loop_exit(self.ptr) #zamyka okno

    def show(self):
        self.mlx.mlx_loop_hook(self.ptr, self.draw_window, None)
        #self.mlx.mlx_loop_hook(self.ptr, schlang(self.mlx, self.window, self.ptr), self)
        self.mlx.mlx_loop(self.ptr)


if __name__ == "__main__":
    window = Window("output.txt")
    window.show()
