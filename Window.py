from mlx import Mlx
from DrawMaze import Maze
from Image import Image
from Button import Button
from typing import List, Optional, Tuple, Any
from MazeGenerator import MazeGenerator
from Maze import Maze as Maze2
from MazeSolver import MazeSolver


class Window():

    def __init__(self, output: str | None = None, maze_width: int = 10,
                 maze_height: int = 10, entry: Tuple[int, int] = (0, 0),
                 exit: Tuple[int, int] = (10, 10),
                 path: List[Tuple[int, int]] | None = None) -> None:
        self.mlx: Mlx = Mlx()
        self.ptr = self.mlx.mlx_init()

        __, width, height = self.mlx.mlx_get_screen_size(self.ptr)
        self.color = bytes([255, 255, 255, 255])

        self.window = self.mlx.mlx_new_window(
            self.ptr, width, height, "whoores"
            )

        self.output = output
        self.path_show = False

        self.path = path

        self.entry = entry
        self.exit = exit

        self.maze = Maze(self.mlx, self.ptr, self.window, output,
                         maze_width, maze_height, entry, exit, path)

        self.mlx.mlx_hook(self.window, 33, 0, self.close, None)
        self.mlx.mlx_hook(self.window, 4, 1 << 2, self.mouse_click, None)
        self.mlx.mlx_key_hook(self.window, self.key_event, None)
        self.papa = True

    def key_event(self, key: int, param: Any) -> None:
        if key == 65307:
            self.close()
        elif key == 112:
            if self.path_show:
                self.path_show = False
                self.maze.draw_path(bytes([0, 255, 255, 255]))
            else:
                self.path_show = True
                self.maze.draw_path(bytes([0, 0, 0, 255]))
        elif key == 106:
            self.papei.show = not self.papei.show
            self.papei.show_button()
        elif key == 65363:
            self.button_width.update_int(1, 150, 10)
        elif key == 65361:
            self.button_width.update_int(-1, 150, 10)
        elif key == 65293:
            self.maze.clear_image()
            if (int(self.button_width.word) == self.maze.width
                    and int(self.button_height.word) == self.maze.height):
                maze = Maze2(self.maze.width, self.maze.height,
                             self.maze.entry, self.maze.exit, False)
            else:
                self.maze.width = int(self.button_width.word)
                self.maze.height = int(self.button_height.word)
                maze = Maze2(self.maze.width, self.maze.height, (0, 0),
                             (self.maze.width - 1, self.maze.height - 1),
                             False)
                self.maze.entry = (0, 0)
                self.maze.exit = (self.maze.width - 1, self.maze.height - 1)
                self.maze.update_size()
                self.button_size.word = str(self.maze.size)
                self.button_size.put_str()
            solver = MazeSolver()
            self.maze.output = maze_gen.cerate_maze(maze)
            self.maze.path = solver.solve_maze(maze)
            self.redraw()
        elif key == 65362:
            self.button_height.update_int(1, 150, 10)
        elif key == 65364:
            self.button_height.update_int(-1, 150, 10)

    def mouse_click(self, button: int, x: int, y: int, param: Any) -> None:
        if button == 4:
            size = self.button_size.update_int(1, self.maze.max)
            if self.maze.size != size:
                self.maze.size = size
                self.redraw()
        if button == 5:
            size = self.button_size.update_int(-1, self.maze.max)
            if self.maze.size != size:
                self.maze.size = size
                self.redraw()
        if ((x >= 1600 and x < 1834) and (y >= 630 and y < 829)):
            pixelx = x - 1600
            pixely = y - 630
            color = self.button.color_data[
                pixely * self.button.size_line + 4 * pixelx:
                pixely * self.button.size_line + 4 * (pixelx + 1)
                ]
            if button == 1:
                if self.color != color and color != bytes([0, 0, 0, 0]):
                    self.color = color
                    self.redraw()
            elif button == 3:
                if color != bytes([0, 0, 0, 0]):
                    self.maze.draw_fourtytwo(color)
                    self.maze.put_maze_to_window()

    def redraw(self) -> None:
        self.maze.clear_image()
        self.maze.draw_maze(self.color)
        self.maze.draw_path(bytes([0, 255, 255, 255]))

    def close(self, param: Any) -> None:
        self.mlx.mlx_destroy_window(self.ptr, self.window)
        self.mlx.mlx_loop_exit(self.ptr)

    def show(self) -> None:
        self.button = Image(self.ptr, self.window, self.mlx, 1600, 630)
        self.papei = Image(self.ptr, self.window, self.mlx, 170, 720,
                           "images/4837205_print_1.png", False)
        self.mouse_left = Image(self.ptr, self.window, self.mlx, 1640, 488,
                                "images/mouse.png")
        self.mouse_right = Image(self.ptr, self.window, self.mlx, 1730, 500,
                                 "images/42colormouse.png")
        self.regenerate = Image(self.ptr, self.window, self.mlx, 1730, 919,
                                "images/enter.png")
        self.mlx.mlx_string_put(self.ptr, self.window, 1650, 845, 0xFFFFFF,
                                "Scale:")
        self.p_key = Image(self.ptr, self.window, self.mlx, 1680, 390,
                           "images/keyboard_key_p.png")
        self.button_size = Button(self.ptr, self.window, self.mlx, 1720, 845,
                                  70, 20, self.maze.size)
        self.mlx.mlx_string_put(self.ptr, self.window, 1610, 931, 0xFFFFFF,
                                "Height:")
        self.up_key = Image(self.ptr, self.window, self.mlx, 1686, 891,
                            "images/keyboard_key_up.png", True)
        self.down_key = Image(self.ptr, self.window, self.mlx, 1686, 971,
                              "images/keyboard_key_down.png", True)
        self.button_height = Button(self.ptr, self.window, self.mlx, 1686, 916,
                                    20, 50, self.maze.height)
        self.mlx.mlx_string_put(self.ptr, self.window, 1520, 931, 0xFFFFFF,
                                "Width:")
        self.button_width = Button(self.ptr, self.window, self.mlx, 1523, 956,
                                   50, 20, self.maze.width)
        self.left_key = Image(self.ptr, self.window, self.mlx, 1500, 956,
                              "images/keyboard_key_left.png", True)
        self.right_key = Image(self.ptr, self.window, self.mlx, 1576, 956,
                               "images/keyboard_key_right.png", True)
        #self.mlx.mlx_loop_hook(self.ptr, self.maze.draw_maze(), None) <- animacja

        self.up_key.show_button()
        self.down_key.show_button()
        self.button.show_button()
        self.maze.draw_maze(bytes([255, 255, 255, 255]))
        self.right_key.show_button()
        self.left_key.show_button()
        self.mouse_left.show_button()
        self.p_key.show_button()
        self.mouse_right.show_button()
        self.regenerate.show_button()
        self.mlx.mlx_loop(self.ptr)


if __name__ == "__main__":
    maze_gen = MazeGenerator()
    maze = Maze2(10, 10, (0, 0), (4, 2), False)
    output = maze_gen.cerate_maze(maze, 1)
    solver = MazeSolver()
    window = Window(output, maze.width, maze.height, maze.entry,
                    maze.exit, solver.solve_maze(maze))
    window.show()
