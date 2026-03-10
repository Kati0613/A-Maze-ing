from mlx import Mlx
import time
#from schlang import draw_schlang as schlang


class Window():

    def __init__(self, output = None):
        self.mlx = Mlx()
        self.ptr = self.mlx.mlx_init()
        self.x = 0
        self.y = 0
        self.i = 0
        self.z = 0

        validator, width, height = self.mlx.mlx_get_screen_size(self.ptr)

        if validator != 0:
            print("Błąd przy pobieraniu rozmiaru ekranu")

        print(width)
        print(height)


        self.window = self.mlx.mlx_new_window(
            self.ptr, width, height, "whoores"
            )

        self.output = output

        file = open("output.txt")
        self.lines = file.readlines()
        self.width_img = len(self.lines[0]) - 1
        self.height_img = len(self.lines) - 4
        self.size = 32
        self.img_ptr = self.mlx.mlx_new_image(self.ptr, self.width_img * self.size, (self.height_img + 1) * (self.size - 1)) # 800 to piksele czyli jeden piksel to 4 bity czyli jeden bajt
        self.mlx_img_data = self.mlx.mlx_get_data_addr(self.img_ptr)
        print(self.width_img)
        print(self.height_img)
        print(f"Dlugosc obrazu: {(self.height_img + 1) * (self.size - 1)}")
        self.image_data = self.mlx_img_data[0]
        self.line_length = self.mlx_img_data[2]
        # self.image_data[:] = bytes([0, 0, 0, 255]) * (len(self.image_data)//4)
        # self.image_data[0:self.line_length] = bytes([255 , 255, 255, 255]) * (self.mlx_img_data[2] // 4)
        self.mlx.mlx_put_image_to_window(self.ptr, self.window, self.img_ptr, 560, 140)
        self.mlx.mlx_hook(self.window, 33, 0, self.close, None)
        self.mlx.mlx_key_hook(self.window, self.key_event, None)

        #       pixel = format(int("3", 16), "04b")

        #schlang(self.mlx, self.window, self.ptr)

    def key_event(self, key, param):
        if key == 65307:  #bash xav do sprawdzenia
            self.close(None)
    
    def draw_pixel(self, pixel = None):
        for line in self.lines[:-4]:
            self.x = 0
            for px in line[:-1]:
                pixel = format(int(px,16),"04b")
                if pixel[0] == "1":
                    self.image_data[self.y*self.line_length + 4 * self.x: self.y*self.line_length + 4*(self.x + self.size)] = self.size * bytes([255,255,255,255])#gorna sciana
                for i in range(0, self.size - 1):
                    if pixel[3] == "1":
                        self.image_data[(self.y + i) * self.line_length + 4 * self.x: (self.y + i) * self.line_length + 4 *(self.x + 1)] = bytes([255,255,255,255])#lewa sciana
                    if pixel[1] == "1":
                        self.image_data[(self.y + i) * self.line_length + 4* (self.x + self.size - 1): (self.y + i) * self.line_length + 4 *(self.x + self.size)] = bytes([255,255,255,255])#prawa sciana
                        print(f"Prawa scianka : { (self.y + i) * self.line_length + 4 *(self.x + self.size)}")
                if pixel[2] == "1":
                    self.image_data[(self.y+self.size - 1)*self.line_length + 4 * self.x: (self.y+ self.size - 1)*self.line_length + 4*(self.x + self.size)] = self.size * bytes([255,255,255,255])#dolna sciana
                    #print(f"Dolna scianka : {self.y+self.size - 1}")
                if pixel == "1111":
                     for i in range(1, self.size - 2):
                         self.image_data[(self.y + i) * self.line_length + 4 * self.x: (self.y + i) * self.line_length + 4 *(self.x + self.size - 2)] = (self.size - 2) * bytes([255,255,255,50])
                self.x += self.size  
            #break
            self.y += self.size - 1
        print(self.x)
        print(f"Y equals: {self.y}")
        self.mlx.mlx_put_image_to_window( self.ptr, self.window, self.img_ptr, 560, 140)
    
    def draw_maze(self, param):
        #self.draw_window()
        first_line = self.lines[0]
        for px in first_line:
            pixel = format(int(px,16),)
 
    def draw_window(self, param):
        #print((self.width_img * self.height_img - 2) * size)
        #print(32 * (self.width_img * self.height_img - 2))
        if self.i < self.x:
            self.image_data[4*self.i: 4 * (self.i + 1)] = bytes([255, 255, 255, 255])
            self.image_data[(self.y) * self.line_length + 4*self.i: (self.y) * self.line_length + 4 * (self.i + 1)] = bytes([255, 255, 255, 255])
        if self.z < self.y:
            self.image_data[self.z*self.line_length + 4*0:
                            self.z*self.line_length + 4 * (0 + 1)] =  bytes([255, 255, 255, 255])
            self.image_data[self.z*self.line_length + 4*799:
                            self.z*self.line_length + 4 * (799 + 1)] = bytes([255, 255, 255, 255])
        self.mlx.mlx_put_image_to_window( self.ptr, self.window, self.img_ptr, 560, 140)
        self.i += 1 #temporary x
        self.z += 1 #temporary 
    
    #def make_schlang_bigger(self):
    def close(self, param):
        self.mlx.mlx_destroy_window(self.ptr, self.window)
        self.mlx.mlx_loop_exit(self.ptr) #zamyka okno

    def show(self):
        self.draw_pixel()
        #self.mlx.mlx_loop_hook(self.ptr, self.draw_pixel, None)
        self.mlx.mlx_loop_hook(self.ptr, self.draw_window, None)
        #self.mlx.mlx_loop_hook(self.ptr, schlang(self.mlx, self.window, self.ptr), self)
        self.mlx.mlx_loop(self.ptr)


if __name__ == "__main__":
    window = Window("output2.txt")
    window.show()
