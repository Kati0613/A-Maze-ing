from typing import List
from maze import Maze
from MazeGenerator import MazeGenerator

class MazeSolver:
    def preper_data(self, maze: Maze):
        self.maze_map = maze.maze_map
        self.width = maze.width
        self.height = maze.height
        self.entry = maze.entry[1] * self.height + maze.entry[0]
        self.exit = maze.exit[1] * self.height + maze.exit[0]
        self.queue = []
        self.visited = set()
        self.came_from = []

    def solve_maze(self, maze: Maze):
        self.preper_data(maze)
        self.queue.append(self.entry)
        self.visited.add(self.entry)

        while (self.queue)
            current = self.queue.pop(0)
            if current == self.exit:
                break
            neighbors = self.check_neighbors(current)
            for n in neighbors:
                if n not in visited:
                    self.visited.add(n)
                    self.queue.append(n)
                    self.came_from[n] = current
        
        path = []
        current = exit

        while current != entry:
            path.append(current)
            current = came_from[current]

        path.append(entry)
        path.reverse()
        print(path)

    def check_neighbors(self, current: int):
        neighbors = []
        x = current % self.width
        y = current // self.width

        # góra
        if not (self.maze_map[current] & 0b0001):
            neighbors.append(current - width)

        # dół
        if not (self.maze_map[current] & 0b0100):
            neighbors.append(current + width)

        # lewo
        if not (self.maze_map[current] & 0b1000):
            neighbors.append(current - 1)

        # prawo
        if not (self.maze_map[current] & 0b0010):
            neighbors.append(current + 1)
        
        return neighbors

if __name__ == "__main__":
    maze = Maze(9, 9, (0, 0), (9, 9), True)
    gen = MazeGenerator()
    
    solver = MazeSolver()