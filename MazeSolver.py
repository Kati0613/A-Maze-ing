from typing import List

class MazeSolver:
    def __init__(self, maze_map: List[int], width: int, height: int):
        self.maze_map = maze_map
        self.width = width
        self.height = height