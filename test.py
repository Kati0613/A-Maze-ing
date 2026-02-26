from mlx import Mlx


class Window():

    def __init__(self):
        self.mlx = Mlx()
        self.ptr = self.mlx.mlx_init()
        self.window = self.mlx.mlx_new_window(
            self.ptr, 800, 800, "whoores"
            )
        self.mlx.mlx_pixel_put(self.ptr, self.window, 200, 200, 0xFFFF00)
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
