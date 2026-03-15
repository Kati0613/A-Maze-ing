from mlx import Mlx


class Button():

    def __init__(self):
        self.btn_ptr = self.mlx.mlx_new_image(self.ptr, 100, 100)
        self.mlx_btn_data = self.mlx.mlx_get_data_addr(self.btn_ptr)
        self.btn_data = self.mlx_btn_data[0]
        self.btn_data[0:4 * 100 * 100] = 100 * 100 * bytes([0, 255, 255, 255])

        return self.btn_ptr
    
    