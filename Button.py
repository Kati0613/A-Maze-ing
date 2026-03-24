from mlx import Mlx


class Button():

    def __init__(self, ptr, window, mlx):
        self.btn_ptr = mlx.mlx_new_image(ptr, 100, 100)
        self.mlx_btn_data = mlx.mlx_get_data_addr(self.btn_ptr)
        self.btn_data = self.mlx_btn_data[0]
        img_array = mlx.mlx_png_file_to_image(ptr, "image.png")

        img_data = mlx.mlx_get_data_addr(img_array[0])
        self.color_data = bytes(img_data[0])
        self.color_lenth = img_data[2]

        self.image_data_ptr = img_array[0]

        mlx.mlx_put_image_to_window(ptr, window, img_array[0], 1600, 800)

    