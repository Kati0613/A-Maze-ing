#from Window import Window
from typing import Any
from mlx import Mlx


class Button():

    def __init__(self, ptr: Any, window: Any, mlx: Mlx, x: int = 1600,
                 y: int = 800,
                 width: int = 300, height: int = 300,
                 word: str | None = None) -> None:
        self.ptr = ptr
        self.mlx = mlx
        self.window = window

        self.x = x
        self.y = y

        self.word = str(word)

        self.btn_ptr = self.mlx.mlx_new_image(self.ptr, width, height)
        self.image_data = self.mlx.mlx_get_data_addr(self.btn_ptr)[0]
        self.width = width
        self.height = height
        self.image_data[:] = (
            len(self.image_data) // 4 * bytes([153, 204, 255, 255])
        )

        self.mlx.mlx_put_image_to_window(self.ptr, self.window,
                                         self.btn_ptr, x, y)
        if str is not None:
            self.put_str()

    def put_str(self) -> None:
        self.image_data[:] = (
            len(self.image_data) // 4 * bytes([153, 204, 255, 255])
        )
        self.mlx.mlx_put_image_to_window(self.ptr, self.window,
                                         self.btn_ptr, self.x, self.y)
        self.mlx.mlx_string_put(self.ptr, self.window,
                                self.x + self.width // 2 - 5 * len(self.word),
                                self.y + self.height // 2 - 10,
                                0x000000, self.word)

    def update_int(self, sub: int,
                   maximum: int = 103, minimum: int = 2) -> int:
        counter = min(max(int(self.word) + sub, minimum), maximum)
        self.word = str(counter)
        self.mlx.mlx_put_image_to_window(self.ptr, self.window,
                                         self.btn_ptr, self.x, self.y)
        self.mlx.mlx_string_put(self.ptr, self.window,
                                self.x + self.width // 2 - 5 * len(self.word),
                                self.y + self.height // 2 - 10, 0x000000,
                                self.word)
        return counter

    def refresh(self) -> None:
        self.mlx.mlx_put_image_to_window(self.ptr, self.window, self.btn_ptr,
                                         self.x, self.y)
        if str is not None:
            self.put_str()
