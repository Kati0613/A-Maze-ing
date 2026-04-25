from typing import List, Tuple


def is_valid_maze_dimension(value: int) -> bool:
    return 2 <= value <= 150


class Maze:
    def __init__(
        self,
        width: int,
        height: int,
        entry: Tuple[int, int],
        exit: Tuple[int, int],
        is_perfect: bool,
    ) -> None:
        """Initialize maze dimensions,
        entry/exit positions and generation mode.

        Args:
            width: Maze width in cells.
            height: Maze height in cells.
            entry: Entry coordinate as (x, y).
            exit: Exit coordinate as (x, y).
            is_perfect: If True, the maze should remain perfect
                (single path between cells).

        Raises:
            TypeError: If provided argument types are invalid.
            ValueError: If provided values are out of allowed range.
        """
        if type(width) is not int:
            raise TypeError("Width must be an integer")
        if type(height) is not int:
            raise TypeError("Height must be an integer")
        if not is_valid_maze_dimension(width):
            raise ValueError("Width must be in range 2-150")
        if not is_valid_maze_dimension(height):
            raise ValueError("Height must be in range 2-150")

        if not isinstance(entry, tuple) or len(entry) != 2:
            raise TypeError("Entry must be a tuple of two integers")
        if not isinstance(exit, tuple) or len(exit) != 2:
            raise TypeError("Exit must be a tuple of two integers")
        if type(entry[0]) is not int or type(entry[1]) is not int:
            raise TypeError("Entry coordinates must be integers")
        if type(exit[0]) is not int or type(exit[1]) is not int:
            raise TypeError("Exit coordinates must be integers")
        if entry[0] < 0 or entry[1] < 0:
            raise ValueError("Entry coordinates cannot be negative")
        if exit[0] < 0 or exit[1] < 0:
            raise ValueError("Exit coordinates cannot be negative")
        if entry == exit:
            raise ValueError("Entry and exit cannot be the same")
        if type(is_perfect) is not bool:
            raise TypeError("is_perfect must be a boolean")

        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        if entry[0] >= self.width or entry[1] >= self.height:
            raise ValueError("Entry is outside the maze")
        else:
            self.start = entry[1] * width + entry[0]
        if exit[0] >= self.width or exit[1] >= self.height:
            raise ValueError("Exit is outside the maze")
        else:
            self.end = (exit[1] - 1) * width + exit[0] - 1
        self.is_perfect = is_perfect
        self.map: List[int] = []
