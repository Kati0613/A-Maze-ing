from typing import List, Tuple

class Maze:
    def __init__(self, width: int, height: int, entry: Tuple[int, int], exit: Tuple[int, int], is_perfect: bool) -> None:
        self.width = width
        self.height = height
        self.entry = entry[1] * width + entry[0]
        self.exit = (exit[1] - 1) * width + exit[0] - 1
        self.is_perfect = is_perfect
        self.map: List[int] = []