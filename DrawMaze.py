from typing import Any, Tuple
from mlx import Mlx


class Maze():

    def __init__(self, mlx: Mlx, ptr: Any, window: Any, output: str,
                 width: int, height: int, entry: Tuple[int, int],
                 exit: Tuple[int, int], path: str) -> None:
        self.mlx = mlx
        self.window = window
        self.ptr = ptr
        self.fourtytwo = []
        self.fourtytwo_color = bytes([0, 0, 0, 70])

        self.x = 0
        self.y = 0
        self.i = 0
        self.z = 0

        self.path = path

        self.color = bytes([255, 255, 255, 255])
        self.color_42 = bytes([255, 255, 255, 255])

        self.output = output
        self.width = width
        self.height = height

        self.entry = entry
        self.exit = exit

        if width >= height:
            self.size = round(870/width + 1.2)
            self.max = round(919.15/width + 0.872)
        else:
            self.size = round(870 / height + 1.2)
            self.max = round(919.15 / height + 0.872)

    def update_size(self) -> None:
        if self.width >= self.height:
            self.size = round(870/self.width + 1.2)
            self.max = round(919.15/self.width + 0.872)
        else:
            self.size = round(870 / self.height + 1.2)
            self.max = round(919.15 / self.height + 0.872)

    def draw_maze(self, color: bytes = bytes([255, 255, 255, 255])) -> None:

        self.fourtytwo = []

        cell = self.size - 1
        img_w = self.width * cell + 1
        img_h = self.height * cell + 1

        self.img_ptr = self.mlx.mlx_new_image(self.ptr, img_w, img_h)
        self.mlx_img_data = self.mlx.mlx_get_data_addr(self.img_ptr)
        self.image_data = self.mlx_img_data[0]
        self.line_length = self.mlx_img_data[2]

        # Szybkie czyszczenie - używamy bytes o tej samej długości
        self.image_data[:] = len(self.image_data) // 4 * bytes([0, 0, 0, 255])

        x, y, j = 0, 0, 0

        while y < self.height:
            pixel = self.output[j:j+4]
            if pixel[3] == "1":  # gorna
                start = y * cell * self.line_length + 4 * x * cell
                end = y * cell * self.line_length + (cell * x + cell + 1) * 4
                self.image_data[
                    start: end
                     ] = self.size * color
            if pixel[1] == "1":
                start = (y + 1) * cell * self.line_length + x * cell * 4
                end = (
                    (y + 1) * cell * self.line_length +
                    (cell * x + cell + 1) * 4
                )
                self.image_data[
                    start: end
                     ] = self.size * color
            if pixel[0] == "1":
                for i in range(0, cell):
                    start = (y * cell + i) * self.line_length + x * cell * 4
                    end = (y * cell + i) * self.line_length + x*cell * 4 + 4
                    self.image_data[
                            start: end
                            ] = color
            if pixel[2] == "1":
                for i in range(0, cell):
                    start = (
                        (y * cell + i) * self.line_length + (x + 1) * 4 * cell
                    )
                    end = (
                        (y * cell + i) * self.line_length
                        + (x + 1) * 4 * cell + 4
                    )
                    self.image_data[
                            start: end
                            ] = color
            if pixel == "1111":
                self.fourtytwo.append([x, y])
            if x == self.width - 1:
                x = -1
                y += 1
            j += 4
            x += 1
        self.draw_fourtytwo()

        self.draw_entry()

        self.mlx.mlx_put_image_to_window(self.ptr, self.window,
                                         self.img_ptr, 520, 50)

    def clear_image(self) -> None:
        self.image_data[:] = (
            len(self.image_data) // 4 * bytes([0, 0, 0, 255])
        )

        self.mlx.mlx_put_image_to_window(self.ptr, self.window,
                                         self.img_ptr, 520, 50)

    def put_maze_to_window(self) -> None:
        self.mlx.mlx_put_image_to_window(self.ptr, self.window,
                                         self.img_ptr, 520, 50)

    def draw_fourtytwo(self, color: bytes = None) -> None:
        cell = self.size - 1

        if color:
            self.color_42 = color

        for coor in self.fourtytwo:
            x, y = coor

            base_y = y * cell * self.line_length
            base_x = x * cell * 4

            for i in range(1, cell - 1):
                row = base_y + i * self.line_length

                start = row + base_x + 2 * 4
                end = row + base_x + (cell - 1) * 4

                self.image_data[start:end] = (cell - 3) * self.color_42

    def draw_entry(self, color_start: bytes = bytes([170, 125, 125, 255]),
                   color_end: bytes = bytes([255, 0, 125, 255])) -> None:
        cell = self.size - 1

        start_x, start_y = self.entry
        end_x, end_y = self.exit

        base_start_y = start_y * cell * self.line_length
        base_start_x = start_x * cell * 4

        base_end_y = end_y * cell * self.line_length
        base_end_x = end_x * cell * 4

        for i in range(2, cell - 2):
            row = base_start_y + i * self.line_length

            start = row + base_start_x + 2 * 4
            end = row + base_start_x + (cell - 2) * 4

            self.image_data[start:end] = (cell - 4) * color_start

            row = base_end_y + i * self.line_length

            start = row + base_end_x + 2 * 4
            end = row + base_end_x + (cell - 2) * 4

            self.image_data[start:end] = (cell - 4) * color_end

    def draw_path(self, color: bytes = bytes([0, 255, 255, 255])) -> None:
        cell = self.size - 1

        start_x, start_y = self.entry

        y = start_y * cell * self.line_length
        x = start_x * cell * 4

        path = self.path[1:-1]

        for coor in path:
            y = coor[1] * (self.size - 1)
            x = coor[0] * (self.size - 1)
            for i in range(3, self.size - 2):
                self.image_data[
                    (y + i) * self.line_length
                    + 4 * (x + 2):
                    (y + i) * self.line_length
                    + 4 * (x + self.size - 3)
                    ] = (self.size - 5) * color

        self.mlx.mlx_put_image_to_window(
            self.ptr, self.window, self.img_ptr, 520, 50)
