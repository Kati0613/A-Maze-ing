from mlx import Mlx


class Button():

    def __init__(self, ptr, window, mlx, x = 1600, y= 800, img = "image.png", show = True):
        self.btn_ptr = mlx.mlx_new_image(ptr, 100, 100)
        self.mlx_btn_data = mlx.mlx_get_data_addr(self.btn_ptr)
        self.btn_data = self.mlx_btn_data[0]
        img_array = mlx.mlx_png_file_to_image(ptr, img)

        self.original_image = mlx.mlx_png_file_to_image(ptr, img)[0]

        self.ptr = ptr
        self.img = img
        self.mlx = mlx
        self.window = window

        self.img_data = mlx.mlx_get_data_addr(img_array[0])
        self.color_data = bytes(self.img_data[0])
        self.size_line = self.img_data[2]
        self.x = x
        self.y = y

        self.image_data_ptr = img_array[0]


        self.show = show
            
    def show_button(self):
        if self.show == True:
            self.mlx.mlx_png_file_to_image(self.ptr, self.img)
            self.mlx.mlx_put_image_to_window(self.ptr, self.window, self.original_image, self.x, self.y)
        else:
            self.erase_button()
    
    def erase_button(self):
        buffer = self.img_data[0]
        buffer[:] = bytes([0, 0, 0, 255]) * (len(self.color_data) // 4)
        self.mlx.mlx_put_image_to_window(self.ptr, self.window, self.image_data_ptr, self.x, self.y)


