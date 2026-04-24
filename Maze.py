from typing import List, Tuple


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
            ValueError: If entry or exit are outside maze boundaries.
        """
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
