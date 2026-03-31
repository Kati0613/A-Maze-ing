from mlx import Mlx


class Button():

    def __init__(self, ptr, window, mlx, x = 1600, y= 800, width = 300, height = 300, str = None):
        self.ptr = ptr
        self.mlx = mlx
        self.window = window
        
        self.btn_ptr = self.mlx.mlx_new_image(self.ptr, width, height)
        self.image_data = self.mlx.mlx_get_data_addr(self.btn_ptr)[0]
        self.width = width
        self.height = height
        self.image_data[:] = len(self.image_data) // 4 * bytes([244, 164, 96, 255])

        self.mlx.mlx_put_image_to_window(self.ptr, self.window, self.btn_ptr, x, y)
        if str is not None:
            self.put_str(x, y, str)
        
    
    def put_str(self, x, y, str):
        self.mlx.mlx_string_put(self.ptr, self.window, x + self.width // 2 - 5 * len(str), y + self.height // 2 - 10, 0x000000, str)
        
        