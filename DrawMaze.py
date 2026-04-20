from typing import Any, Tuple, List
from mlx import Mlx


class Maze():
    """Represents a drawable maze rendered inside an MLX window.

    This class stores maze configuration, rendering parameters, and image
    buffers used to draw the maze, its special cells, entry and exit points,
    and the solved path.

    Attributes:
        mlx (Mlx): MLX wrapper used for image and window operations.
        window (Any): Window where the maze image is displayed.
        ptr (Any): Pointer returned by the MLX initialization.
        fourtytwo_color (bytes): Default RGBA color used for special cells.
        path (List[Tuple[int, int]]): Solved path through the maze.
        color (bytes): Default RGBA wall color.
        color_42 (bytes): Current RGBA color for special cells.
        output (str): Encoded maze representation, where each cell is described
            by four characters representing walls.
        width (int): Maze width in cells.
        height (int): Maze height in cells.
        entry (Tuple[int, int]): Coordinates of the maze entry cell.
        exit (Tuple[int, int]): Coordinates of the maze exit cell.
        size (int): Current drawing size of one maze cell.
        max (int): Maximum allowed cell size for rendering.
    """
    @staticmethod
    def generator(tab):
        for element in tab:
            yield element

    def __init__(self, mlx: Mlx, ptr: Any, window: Any, output: str,
                 width: int, height: int, entry: Tuple[int, int],
                 exit: Tuple[int, int], path: List[Tuple[int, int]]
                 ) -> None:
        """Initialize a maze object with rendering and layout information.

        Args:
            mlx (Mlx): MLX wrapper used for drawing operations.
            ptr (Any): Pointer returned by the MLX initialization.
            window (Any): Window where the maze will be displayed.
            output (str): Encoded string describing all maze walls.
            width (int): Width of the maze in cells.
            height (int): Height of the maze in cells.
            entry (Tuple[int, int]): Entry cell coordinates.
            exit (Tuple[int, int]): Exit cell coordinates.
            path (List[Tuple[int, int]]): Solved path through the maze.

        Returns:
            None
        """

        self.mlx = mlx
        self.window = window
        self.ptr = ptr
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

        self.gen = self.generator(self.path[1:-1])

        if width >= height:
            self.size = round(870/width + 1.2)
            self.max = round(919.15/width + 0.872)
        else:
            self.size = round(870 / height + 1.2)
            self.max = round(919.15 / height + 0.872)
        self.cell = self.size - 1

        self.animating = True

    def update_size(self) -> None:
        """Recalculate cell size and maximum scale based on maze dimensions.

        The method adjusts `size` and `max` so the maze can still fit into
        the rendering area after changing its width or height.

        Returns:
            None
        """
        if self.width >= self.height:
            self.size = round(870/self.width + 1.2)
            self.max = round(919.15/self.width + 0.872)
        else:
            self.size = round(870 / self.height + 1.2)
            self.max = round(919.15 / self.height + 0.872)
        self.cell = self.size - 1

    def draw_maze(self, color: bytes = bytes([255, 255, 255, 255])) -> None:
        """Draw the full maze into an image buffer and display it in the
        window.

        This method creates a new image, clears it, draws maze walls based on
        the encoded `output` string, marks special cells, draws entry and exit
        points, and finally places the rendered image in the window.

        Args:
            color (bytes, optional): RGBA color used to draw maze walls.
                Defaults to white.

        Returns:
            None
        """
        self.fourtytwo = []

        self.cell = self.size - 1
        img_w = self.width * self.cell + 1
        img_h = self.height * self.cell + 1

        self.window_pos_x = int((1920 - img_w) / 2)
        self.window_pos_y = int((1080 - img_h) / 2) - 30

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
                start = y * self.cell * self.line_length + 4 * x * self.cell
                end = y * self.cell * self.line_length + (self.cell * x + self.cell + 1) * 4
                self.image_data[
                    start: end
                     ] = self.size * color
            if pixel[1] == "1":
                start = (y + 1) * self.cell * self.line_length + x * self.cell * 4
                end = (
                    (y + 1) * self.cell * self.line_length +
                    (self.cell * x + self.cell + 1) * 4
                )
                self.image_data[
                    start: end
                     ] = self.size * color
            if pixel[0] == "1":
                for i in range(0, self.cell):
                    start = (y * self.cell + i) * self.line_length + x * self.cell * 4
                    end = (y * self.cell + i) * self.line_length + x*self.cell * 4 + 4
                    self.image_data[
                            start: end
                            ] = color
            if pixel[2] == "1":
                for i in range(0, self.cell):
                    start = (
                        (y * self.cell + i) * self.line_length + (x + 1) * 4 * self.cell
                    )
                    end = (
                        (y * self.cell + i) * self.line_length
                        + (x + 1) * 4 * self.cell + 4
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
                                         self.img_ptr, self.window_pos_x,
                                         self.window_pos_y)

    def clear_image(self) -> None:
        """Clear the current maze image by filling it with a solid background.

        After clearing the image buffer, the updated image is displayed
        in the application window.

        Returns:
            None
        """
        self.image_data[:] = (
            len(self.image_data) // 4 * bytes([0, 0, 0, 255])
        )

        self.put_maze_to_window()

    def put_maze_to_window(self) -> None:
        """Display the current maze image buffer in the application window.

        This method does not redraw the maze. It only places the already
        prepared image into the window.

        Returns:
            None
        """
        self.mlx.mlx_put_image_to_window(self.ptr, self.window,
                                         self.img_ptr, self.window_pos_x,
                                         self.window_pos_y)

    def draw_fourtytwo(self, color: bytes | None = None) -> None:
        """Fill special maze cells with a selected color.

        Special cells are stored in `self.fourtytwo` and are usually detected
        while parsing the encoded maze representation. If a new color is
        passed,
        it becomes the current color for drawing those cells.

        Args:
            color (bytes | None, optional): RGBA color used to fill special
                cells. If None, the previously stored color is used.
                Defaults to None.

        Returns:
            None
        """
        #cell = self.size - 1

        if color:
            self.color_42 = color

        for coor in self.fourtytwo:
            x, y = coor

            base_y = y * self.cell * self.line_length
            base_x = x * self.cell * 4

            for i in range(1, self.cell - 1):
                row = base_y + i * self.line_length

                start = row + base_x + 2 * 4
                end = row + base_x + (self.cell - 1) * 4

                self.image_data[start:end] = (self.cell - 3) * self.color_42

    def draw_entry(self, color_start: bytes = bytes([170, 125, 125, 255]),
                   color_end: bytes = bytes([255, 0, 125, 255])) -> None:
        """Draw the entry and exit cells using dedicated colors.

        The entry cell is filled with `color_start`, while the exit cell
        is filled with `color_end`. This makes both important positions
        visually distinct from the rest of the maze.

        Args:
            color_start (bytes, optional): RGBA fill color for the entry cell.
                Defaults to a muted pink shade.
            color_end (bytes, optional): RGBA fill color for the exit cell.
                Defaults to a bright pink shade.

        Returns:
            None
        """

        start_x, start_y = self.entry
        end_x, end_y = self.exit

        base_start_y = start_y * self.cell * self.line_length
        base_start_x = start_x * self.cell * 4

        base_end_y = end_y * self.cell * self.line_length
        base_end_x = end_x * self.cell * 4

        for i in range(2, self.cell - 2):
            row = base_start_y + i * self.line_length

            start = row + base_start_x + 2 * 4
            end = row + base_start_x + (self.cell - 2) * 4

            self.image_data[start:end] = (self.cell - 4) * color_start

            row = base_end_y + i * self.line_length

            start = row + base_end_x + 2 * 4
            end = row + base_end_x + (self.cell - 2) * 4

            self.image_data[start:end] = (self.cell - 4) * color_end

    def draw_path(self, color: bytes = bytes([0, 255, 255, 255])) -> None:
        """Draw the solved maze path on top of the current maze image.

        The method skips the first and last cells of the stored path so the
        entry and exit remain visually highlighted by `draw_entry()`.

        Args:
            color (bytes, optional): RGBA color used to draw the solution path.
                Defaults to cyan.

        Returns:
            None
        """
        #cell = self.size - 1

        start_x, start_y = self.entry

        y = start_y * self.cell * self.line_length
        x = start_x * self.cell * 4

        path = self.path[1:-1]

        for coor in path:
            y = coor[1] * self.cell
            x = coor[0] * self.cell

            for i in range(1, self.cell - 1):
                self.image_data[
                        (y + i) * self.line_length
                        + 4 * (x + 2):
                        (y + i) * self.line_length
                        + 4 * (x + self.cell - 1)
                ] = (self.cell - 3) * color

        self.put_maze_to_window()

    def reset_animation(self):
        self.gen = self.generator(self.path[1:-1])

    def draw_animated_path(self, param):
        if self.animating:
            try:
                coor = next(self.gen)

                y = coor[1] * self.cell
                x = coor[0] * self.cell

                for i in range(1, self.cell - 1):
                    self.image_data[
                        (y + i) * self.line_length
                        + 4 * (x + 2):
                        (y + i) * self.line_length
                        + 4 * (x + self.cell - 1)
                    ] = (self.cell - 3) * bytes([0, 255, 125, 255])
                self.put_maze_to_window()
            except StopIteration:
                self.animating = False
        return

# row = base_y + i * self.line_length

#                 start = row + base_x + 2 * 4
#                 end = row + base_x + (self.cell - 1) * 4