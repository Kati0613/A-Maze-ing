from mlx import Mlx
from DrawMaze import Maze
from Image import Image
from Button import Button
from typing import List, Tuple, Any, Iterator
from MazeGenerator import MazeGenerator
from Maze import Maze as Maze2
from MazeSolver import MazeSolver


class Window():
    """Represents the main application window used to display and
    interact with a maze.

    This class initializes the graphical window, creates all UI elements,
    handles keyboard and mouse events, and manages maze rendering.

    Attributes:
        mlx (Mlx): MLX wrapper used for graphical operations.
        ptr: Pointer returned by the MLX initialization function.
        color (bytes): Currently selected drawing color in RGBA format.
        window: Handle to the created application window.
        output (str): Text representation of the generated maze.
        path_show (bool): Indicates whether the solved path
        is currently visible.
        path (List[Tuple[int, int]]): Solved path through the maze.
        entry (Tuple[int, int]): Entry coordinates of the maze.
        exit (Tuple[int, int]): Exit coordinates of the maze.
        maze (Maze): Graphical maze object responsible for rendering.
    """

    def __init__(self, output: str, generator: Iterator,
                 maze_width: int = 10,
                 maze_height: int = 10, entry: Tuple[int, int] = (0, 0),
                 exit: Tuple[int, int] = (10, 10),
                 path: List[Tuple[int, int]] = [],
                 ) -> None:
        """Initialize the main application window and all interface elements.

        Args:
            output (str): String representation of the maze layout.
            maze_width (int, optional): Width of the maze in cells. Defaults
            to 10.
            maze_height (int, optional): Height of the maze in cells. Defaults
            to 10.
            entry (Tuple[int, int], optional): Starting cell coordinates.
            Defaults to (0, 0).
            exit (Tuple[int, int], optional): Ending cell coordinates.
            Defaults to (10, 10).
            path (Optional[List[Tuple[int, int]]], optional): Solved maze path.
                Defaults to [].

        Returns:
            None
        """
        self.mlx: Mlx = Mlx()
        self.ptr = self.mlx.mlx_init()

        __, width, height = self.mlx.mlx_get_screen_size(self.ptr)
        self.color = bytes([255, 255, 255, 255])

        self.window = self.mlx.mlx_new_window(
            self.ptr, width, height, "A-maze-ing"
            )

        self.output = output
        self.path_show = True

        self.path = path
        self.generator = generator

        self.entry = entry
        self.exit = exit

        self.maze = Maze(self.mlx, self.ptr, self.window, output,
                         maze_width, maze_height, entry, exit, path, generator)

        self.mlx.mlx_hook(self.window, 33, 0, self.close, None)
        self.mlx.mlx_hook(self.window, 4, 1 << 2, self.mouse_click, None)
        self.mlx.mlx_key_hook(self.window, self.key_event, None)
        self.papa = True

        self.button = Image(self.ptr, self.window, self.mlx, 1600, 630)
        self.papei = Image(self.ptr, self.window, self.mlx, 140, 720,
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
        self.mouse_scroll = Image(self.ptr, self.window, self.mlx, 1800, 825,
                                  "images/scroll.png", True)
        self.amazing_title = Image(self.ptr, self.window, self.mlx, 50, 50,
                                   "images/a-maze-ing-title.png", True)

    def key_event(self, key: int, param: Any = None) -> None:
        """Handle keyboard input events.

        Supported keys include:
            - Escape: closes the window.
            - P: toggles maze path visibility.
            - J: toggles a specific image visibility.
            - Arrow keys: adjust maze dimensions.
            - Enter: regenerates and resolves the maze.

        Args:
            key (int): Integer code of the pressed key.
            param (Any, optional): Additional event parameter passed by MLX.
                Defaults to None.

        Returns:
            None
        """
        if key == 65307:
            self.close(param)
        elif key == 112:
            self.path_show = not self.path_show
            if self.path_show:
                self.maze.draw_path(bytes(([255, 153, 204, 255])))
            else:
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
            self.maze.gen_overlfow = solver.solve_maze_steps(maze)
            self.redraw_animated()
        elif key == 65362:
            self.button_height.update_int(1, 150, 10)
        elif key == 65364:
            self.button_height.update_int(-1, 150, 10)

    def mouse_click(self, button: int, x: int, y: int, param: Any) -> None:
        """Handle mouse click and scroll events.

        This method updates the maze scale when the mouse wheel is used and
        changes the selected drawing color when the color palette is clicked.
        A right mouse click on the palette triggers a 42 drawing action.

        Args:
            button (int): Mouse button or scroll code.
            x (int): X coordinate of the mouse click.
            y (int): Y coordinate of the mouse click.
            param (Any): Additional event parameter passed by MLX.

        Returns:
            None
        """
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

    def redraw_animated(self) -> None:
        """Clear and redraw the maze using the current settings.

        The maze is redrawn with the currently selected color and the path
        is rendered afterward. Path is re-animated.

        Returns:
            None
        """
        self.maze.clear_image()
        self.maze.draw_maze(self.color)
        if self.path_show:
            self.maze.reset_animation()

    def animation(self, param: None = None) -> None:
        """
            Animates the maze generation process and the pathfinding 
            visualization.

            This method first displays the animated maze generation sequence,
            and then shows the animated path traversal using the same optional
            parameter.

            Args:
                param (None, optional):
                    Optional parameter passed to both animation methods.
                    Defaults to None.

            Returns:
                None
        """
        self.maze.draw_animated_generation(param)
        self.maze.draw_animated_path(param)

    def redraw(self) -> None:
        """Clear and redraw the maze using the current settings.

        The maze is redrawn with the currently selected color and the path
        is rendered afterward. Path is rendared without animation.

        Returns:
            None
        """
        self.maze.clear_image()
        self.maze.draw_maze(self.color)
        if self.path_show:
            self.maze.draw_path()

    def close(self, param: Any) -> None:
        """Close the application window and exit the MLX loop.

        Args:
            param (Any): Additional event parameter passed by MLX.

        Returns:
            None
        """
        self.mlx.mlx_destroy_window(self.ptr, self.window)
        self.mlx.mlx_loop_exit(self.ptr)

    def show(self) -> None:
        """Display all UI elements and start the main event loop.

        This method renders the maze and interface buttons, then launches
        the MLX event loop to keep the window responsive.

        Returns:
            None
        """
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
        self.mouse_scroll.show_button()
        self.amazing_title.show_button()
        self.mlx.mlx_loop_hook(self.ptr, self.animation, None)
        self.mlx.mlx_loop(self.ptr)


if __name__ == "__main__":
    maze_gen = MazeGenerator()
    maze = Maze2(20, 20, (0, 0), (9, 9), False)
    output = maze_gen.cerate_maze(maze, 1)
    solver = MazeSolver()
    window = Window(output, solver.solve_maze_steps(maze), maze.width,
                    maze.height, maze.entry, maze.exit, solver.solve_maze(maze)
                    )
    window.show()
