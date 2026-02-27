from mlx import Mlx
import time

class Window():

    def __init__(self):
        self.mlx = Mlx()
        self.ptr = self.mlx.mlx_init()
        self.window = self.mlx.mlx_new_window(
            self.ptr, 800, 800, "whoores"
            )
        
        self.img_ptr = self.mlx.mlx_new_image(self.ptr, 800, 800)
        self.mlx_img_data = self.mlx.mlx_get_data_addr(self.img_ptr)
        print(self.mlx_img_data)
        self.image_data = self.mlx_img_data[0]
        self.image_data[:] = bytes([0,0,0,255]) * (len(self.image_data)//4)
        self.image_data[3200:6400] = bytes([255,255,255,255]) * (self.mlx_img_data[2] // 4)
        self.image_data[3*3200:4*3200] = bytes([255,255,255,255]) * (self.mlx_img_data[2] // 4)

        self.mlx.mlx_put_image_to_window(self.ptr, self.window, self.img_ptr, 0, 0)
        self.mlx.mlx_hook(self.window, 33, 0, self.close, None)
        self.mlx.mlx_key_hook(self.window, self.key_event, None)

    def key_event(self, key, param):
        if key == 65307:  #bash xav do sprawdzenia
            self.close(None)
    
  
      
    def close(self, param):
        self.mlx.mlx_destroy_window(self.ptr, self.window)
        self.mlx.mlx_loop_exit(self.ptr) #zamyka okno

    def show(self):
        self.mlx.mlx_loop(self.ptr)


if __name__ == "__main__":
    window = Window()
    window.show()
