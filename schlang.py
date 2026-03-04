
class Schlang:

    def __init__(self, mlx, window, ptr):
        self.mlx = mlx
        self.window = window
        self.ptr = ptr

    def draw_schlang(self):
        for i in range(1, 51):
            self.mlx.mlx_pixel_put(
                self.ptr, self.window, 374 + i, 200, 0xFFFFFF11)  #bialy
            self.mlx.mlx_pixel_put(
                self.ptr, self.window, 375, 200 + i, 0xFFFFFF11)  #bialy
            self.mlx.mlx_pixel_put(
                self.ptr, self.window, 425, 200 + i, 0xFFFFFF11)
            self.mlx.mlx_pixel_put(
                self.ptr, self.window, 400, 200 + i, 0xFFFFFF11)
            self.mlx.mlx_pixel_put(
                self.ptr, self.window, 374 + i, 250, 0xFFFFFF11)

        for i in range(1, 200):
            self.mlx.mlx_pixel_put(
                self.ptr, self.window, 375, 250 + i, 0xFFFFFF11)  #bialy
            self.mlx.mlx_pixel_put(
                self.ptr, self.window, 425, 250 + i, 0xFFFFFF11)

        for i in range(1, 101):
            self.mlx.mlx_pixel_put(
                self.ptr, self.window, 375 - i, 450, 0xFFFFFF11)
            self.mlx.mlx_pixel_put(
                self.ptr, self.window, 425 + i, 450, 0xFFFFFF11)

        for i in range(1, 101):
            self.mlx.mlx_pixel_put(
                self.ptr, self.window, 275, 450 + i, 0xFFFFFF11)
            self.mlx.mlx_pixel_put(
                self.ptr, self.window, 525, 450 + i, 0xFFFFFF11)

        for i in range(1, 101):
            self.mlx.mlx_pixel_put(
                self.ptr, self.window, 275 + i, 550, 0xFFFFFF11)
            self.mlx.mlx_pixel_put(
                self.ptr, self.window, 525 - i, 550, 0xFFFFFF11)

        for i in range(1, 101):
            self.mlx.mlx_pixel_put(
                self.ptr, self.window, 375, 550 - i, 0xFFFFFF11)
            self.mlx.mlx_pixel_put(
                self.ptr, self.window, 425, 550 - i, 0xFFFFFF11)
   
    def make_schlang_bigger(self):
        for i in range(1, 51):
            for i in range(1, 10):
                self.mlx.mlx_pixel_put(self.ptr, self.window, 374 + i, 200 - i, 0xFFFFFF11)
                self.mlx.mlx_pixel_put(self.ptr, self.window, 374 + i, 250 - i, 0xFFFFFF11)
