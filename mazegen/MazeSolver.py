from typing import Iterator, List, Tuple
from mazegen.Maze import Maze
from mazegen.MazeGenerator import MazeGenerator
from collections import deque


class MazeSolver:
    def prepere_data(self, maze: Maze) -> None:
        """Initialize solver state from the provided maze instance.

        Args:
            maze: Maze object with map data, dimensions and entry/exit
                coordinates.
        """
        self.maze_map = maze.map
        self.width = maze.width
        self.height = maze.height
        self.entry = maze.entry[1] * self.width + maze.entry[0]
        self.exit = maze.exit[1] * self.width + maze.exit[0]
        self.queue: deque = deque()
        self.visited: set = set()
        self.came_from: dict = {}

    def solve_maze(self, maze: Maze, file_name: str) -> List[Tuple[int, int]]:
        """Solve the maze using breadth-first search
        and return full path coordinates.

        Args:
            maze: Maze object to solve.

        Returns:
            List of (x, y) coordinates describing the shortest discovered path.
        """
        self.prepere_data(maze)
        self.queue.append(self.entry)
        self.visited.add(self.entry)

        while self.queue:
            current = self.queue.popleft()
            if current == self.exit:
                break
            neighbors = self.check_neighbors(current)
            for n in neighbors:
                if n not in self.visited:
                    self.visited.add(n)
                    self.queue.append(n)
                    self.came_from[n] = current

        path = []
        current = self.exit

        while current != self.entry:
            path.append(current)
            current = self.came_from[current]

        path.append(self.entry)
        path.reverse()
        self.save_output(file_name, path)
        return self.prepere_output(path)

    def solve_maze_steps(self, maze: Maze) -> Iterator[List[Tuple[int, int]]]:
        """Solve the maze step-by-step and yield newly
        visited cells per BFS iteration.

        Args:
            maze: Maze object to solve.

        Yields:
            List of (x, y) coordinates visited in the current iteration.

        Returns:
            Final path converted to (x, y) coordinates when iteration ends.
        """
        self.prepere_data(maze)
        self.queue.append(self.entry)
        self.visited.add(self.entry)

        while self.queue:
            current = self.queue.popleft()
            visited_new = []
            if current == self.exit:
                break
            neighbors = self.check_neighbors(current)
            for n in neighbors:
                if n not in self.visited:
                    self.visited.add(n)
                    visited_new.append((n % self.width, n // self.width))
                    self.queue.append(n)
                    self.came_from[n] = current
            yield visited_new

        path = []
        current = self.exit

        while current != self.entry:
            path.append(current)
            current = self.came_from[current]

        path.append(self.entry)
        path.reverse()

    def prepere_output(self, path: List[int]) -> List[Tuple[int, int]]:
        """Convert a path of linear cell indices into (x, y) coordinates.

        Args:
            path: List of cell indices.

        Returns:
            List of (x, y) tuples.
        """
        output = []
        for cell in path:
            output.append((cell % self.width, cell // self.width))

        return output

    def save_output(self, file_name: str, path: List[int]) -> None:
        """Serialize path directions and append them to a file.

        Direction mapping:
            N, S, W, E based on consecutive path cells.

        Args:
            file_name: Output file path.
            path: List of path cell indices.
        """
        output = ""
        for i in range(len(path) - 1):
            cell = path[i]

            if cell - path[i + 1] == self.width:
                output += "N"
            elif cell - path[i + 1] == -self.width:
                output += "S"
            elif cell - path[i + 1] == 1:
                output += "W"
            elif cell - path[i + 1] == -1:
                output += "E"

        with open(file_name, "a") as file:
            file.write(output)

    def check_neighbors(self, current: int) -> List[int]:
        """Return reachable neighbors of a cell based on wall bit flags.

        Args:
            current: Current cell index.

        Returns:
            List of neighboring cell indices that can be traversed.
        """
        neighbors = []
        x = current % self.width
        y = current // self.width

        # góra
        if y > 0 and not (self.maze_map[current] & 0b0001):
            neighbors.append(current - self.width)

        # dół
        if y < self.height - 1 and not (self.maze_map[current] & 0b0100):
            neighbors.append(current + self.width)

        # lewo
        if x > 0 and not (self.maze_map[current] & 0b1000):
            neighbors.append(current - 1)

        # prawo
        if x < self.width - 1 and not (self.maze_map[current] & 0b0010):
            neighbors.append(current + 1)

        return neighbors


if __name__ == "__main__":
    maze = Maze(10, 10, (0, 0), (9, 9), True)
    gen = MazeGenerator()

    solver = MazeSolver()
    print(gen.cerate_maze(maze, "test.txt", 1))

    for step in solver.solve_maze_steps(maze):
        print(step)

    print(solver.solve_maze_steps(maze))
