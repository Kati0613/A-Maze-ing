from typing import Tuple
from mazegen.Maze import Maze as Maze2
from mazegen.MazeGenerator import MazeGenerator
from mazegen.MazeSolver import MazeSolver
from Window import Window
import sys


def load_config(
    file_name: str,
) -> Tuple[int, int, Tuple[int, int], Tuple[int, int], str, bool]:
    config = {}

    try:
        with open(file_name, "r") as f:
            for line_number, line in enumerate(f, start=1):
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()

                if not key:
                    raise ValueError(
                        f"Missing key in config at line {line_number}"
                    )
                if not value:
                    raise ValueError(
                        f"Missing value for key '{key}' at line {line_number}"
                    )

                config[key] = value
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Config file not found: {file_name}") from exc

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

    try:
        width = int(config["WIDTH"])
    except ValueError:
        raise ValueError("WIDTH must be an integer")

    try:
        height = int(config["HEIGHT"])
    except ValueError:
        raise ValueError("HEIGHT must be an integer")

    try:
        x, y = config["ENTRY"].split(",")
        entry = (int(x), int(y))
    except ValueError:
        raise ValueError(
            "ENTRY must contain two integers separated by a comma"
        )

    try:
        x, y = config["EXIT"].split(",")
        exit = (int(x), int(y))
    except ValueError:
        raise ValueError(
            "EXIT must contain two integers separated by a comma"
        )

    output_file = config["OUTPUT_FILE"]

    perfect_value = config["PERFECT"].strip().lower()
    if perfect_value not in ("true", "false"):
        raise ValueError('PERFECT must be "true" or "false"')
    perfect = perfect_value == "true"

    return width, height, entry, exit, output_file, perfect


def validate_config(
    width: int,
    height: int,
    entry: Tuple[int, int],
    exit: Tuple[int, int],
    output_file: str,
    perfect: bool,
) -> None:
    # if width < 10 or width > 150:
    #     raise ValueError("Width must be between 10 and 150")
    # if height < 10 or height > 150:
    #     raise ValueError("Height must be between 10 and 150")
    if entry[0] < 0 or entry[1] < 0:
        raise ValueError("Entry coordinates cannot be negative")
    if exit[0] < 0 or exit[1] < 0:
        raise ValueError("Exit coordinates cannot be negative")
    if entry[0] >= width or entry[1] >= height:
        raise ValueError("Entry is outside the maze")
    if exit[0] >= width or exit[1] >= height:
        raise ValueError("Exit is outside the maze")
    if entry == exit:
        raise ValueError("Entry and exit cannot be the same")
    if not output_file.endswith(".txt"):
        raise ValueError("Output file must have a .txt extension")


if __name__ == "__main__":
    config_name = "config.txt"
    if len(sys.argv) < 2:
        raise ValueError("Usage: python a_maze_ing.py <config_file>")

    config_name = sys.argv[1]
    try:
        width, height, entry, exit, output_file, perfect = load_config(
            config_name
        )
        validate_config(
            width, height, entry, exit, output_file, perfect
        )
        maze_gen = MazeGenerator()
        maze = Maze2(width, height, entry, exit, perfect)
        output = maze_gen.cerate_maze(maze, output_file)
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
    except FileNotFoundError as exc:
        print(exc)
        sys.exit(1)
    except ValueError as e:
        print(e)
        sys.exit(1)
