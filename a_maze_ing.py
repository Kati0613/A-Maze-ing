from typing import Tuple
from mazegen.Maze import Maze as Maze2
from mazegen.MazeGenerator import MazeGenerator
from mazegen.MazeSolver import MazeSolver
from Window import Window


def load_config(
    file_name: str,
) -> Tuple[int, int, Tuple[int, int], Tuple[int, int], str, bool]:
    config = {}

    with open(file_name, "r") as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            key, value = line.split("=", 1)
            config[key.strip()] = value.strip()

    required_keys = [
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
    ]

    missing = [key for key in required_keys if key not in config]
    if missing:
        raise ValueError(f"Missing fields in config: {', '.join(missing)}")

    width = int(config["WIDTH"])
    height = int(config["HEIGHT"])

    x, y = config["ENTRY"].split(",")
    entry = (int(x), int(y))
    x, y = config["EXIT"].split(",")
    exit = (int(x), int(y))

    output_file = config["OUTPUT_FILE"]

    perfect = config["PERFECT"].lower() == "true"

    return width, height, entry, exit, output_file, perfect


def validate_config(
    width: int,
    height: int,
    entry: Tuple[int, int],
    exit: Tuple[int, int],
    output_file: str,
    perfect: bool,
) -> None:
    if width < 10:
        raise ValueError("Width must be greater than 9")
    if height < 10:
        raise ValueError("Height must be grater than 9")
    if entry[0] >= width or entry[1] >= height:
        raise ValueError("Entry is outside the maze")
    if exit[0] >= width or exit[1] >= height:
        raise ValueError("Exit is outside the maze")
    if entry == exit:
        raise ValueError("Entry and exit cannot be the same")
    if not output_file.endswith(".txt"):
        raise ValueError("Output file must have a .txt extension")
    if perfect is not True and perfect is not False:
        raise ValueError("Is perfect must be true or false")


if __name__ == "__main__":
    config_name = "config.txt"
    width, height, entry, exit, output_file, perfect = load_config(config_name)
    validate_config(width, height, entry, exit, output_file, perfect)
    maze_gen = MazeGenerator()
    maze = Maze2(width, height, entry, exit, perfect)
    output = maze_gen.cerate_maze(maze, output_file, 1)
    solver = MazeSolver()
    window = Window(
        output,
        solver.solve_maze_steps(maze),
        maze.width,
        maze.height,
        maze.entry,
        maze.exit,
        solver.solve_maze(maze, output_file),
        output_file,
    )
    window.show()
