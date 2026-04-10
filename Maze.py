from typing import List, Tuple

class Maze:
    def __init__(self, width: int, height: int, entry: Tuple[int, int], exit: Tuple[int, int], is_perfect: bool) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        if entry[0] > self.width or entry[1] > self.height:
            raise ValueError("Entry is outside the maze")
            exit()
        else:
            self.start = entry[1] * width + entry[0]
        if exit[0] > self.width or exit[1] > self.height:
            raise ValueError("Exit is outside the maze")
        else:
            self.end = (exit[1] - 1) * width + exit[0] - 1
        self.is_perfect = is_perfect
        self.map: List[int] = []

        