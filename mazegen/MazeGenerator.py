from random import Random, randint
from typing import List, Set, Optional
from mazegen.Maze import Maze


class MazeGenerator:
    def cerate_maze(
        self,
        maze: Maze,
        file_name: str,
        seed: Optional[int] = None
            ) -> str:
        """Generate a maze map and return its bit-string representation.

        Args:
            maze: Maze configuration object with size, entry/exit and
                perfect/imperfect flag.
            seed: Optional random seed. If not provided, a random value
                is generated.

        Returns:
            Concatenated 4-bit representation of all cells in the
                generated maze.
        """
        if seed is None:
            seed = randint(0, 1000)

        self.maze_random = Random()
        self.maze_random.seed(seed)
        self.width = maze.width
        self.height = maze.height
        self.is_perfect = maze.is_perfect
        self.entry = maze.start
        self.exit = maze.end
        self.maze_map: List[int] = [0xF] * (self.width * self.height)
        self.remaining: Set[int] = set(range(self.width * self.height))
        self.pattern: Set[int] = set()

        self.put_42()
        self.wilson()
        if not self.is_perfect:
            self.make_imperfect(0.1)
        self.save_output(file_name)
        maze.map = self.maze_map
        return self.prep_maze_str()

    def make_imperfect(self, probability: float = 0.1) -> None:
        """Randomly remove additional walls to
        create loops in a non-perfect maze.

        Args:
            probability: Chance to remove each candidate wall.
        """
        for cell in range(self.width * self.height):
            if cell in self.pattern:
                continue
            x = cell % self.width
            y = cell // self.width

            # spróbuj usunąć ścianę w prawo
            if x < self.width - 1 and cell + 1 not in self.pattern:
                if self.maze_random.random() < probability:
                    neighbor = cell + 1
                    if not self.creates_large_open_area(cell, neighbor):
                        self.trim_wall(cell, neighbor)

            # spróbuj usunąć ścianę w dół
            if y < self.height - 1 and cell + self.width not in self.pattern:
                if self.maze_random.random() < probability:
                    neighbor = cell + self.width
                    if not self.creates_large_open_area(cell, neighbor):
                        self.trim_wall(cell, neighbor)

    def creates_large_open_area(self, cell: int, neighbor: int) -> bool:
        """Check whether removing a wall creates an undesired open area.

        The function temporarily removes a wall and checks local 3x3 regions,
        and then restores original cell wall states.

        Args:
            cell: Source cell index.
            neighbor: Adjacent cell index.

        Returns:
            True if the simulated wall removal creates a large open area,
                else False.
        """
        original_cell = self.maze_map[cell]
        original_neighbor = self.maze_map[neighbor]

        # symulacja
        self.trim_wall(cell, neighbor)

        # sprawdź tylko lokalny obszar
        result = self.check_3x3_around(cell) or self.check_3x3_around(neighbor)

        # cofnięcie
        self.maze_map[cell] = original_cell
        self.maze_map[neighbor] = original_neighbor

        return result

    def check_3x3_around(self, cell: int) -> bool:
        """Scan nearby coordinates and detect whether any 3x3
        area is fully open.

        Args:
            cell: Cell index around which to scan.

        Returns:
            True if an open 3x3 region is found, otherwise False.
        """
        x = cell % self.width
        y = cell // self.width

        for dy in range(-2, 1):
            for dx in range(-2, 1):
                if self.is_3x3_open(x + dx, y + dy):
                    return True
        return False

    def is_3x3_open(self, x: int, y: int) -> bool:
        """Check if a 3x3 block at (x, y) has no inner walls.

        Args:
            x: Top-left x coordinate.
            y: Top-left y coordinate.

        Returns:
            True when all cells in the 3x3 block are fully open,
                else False.
        """
        if x < 0 or y < 0 or x + 2 >= self.width or y + 2 >= self.height:
            return False

        for dy in range(3):
            for dx in range(3):
                cell = (y + dy) * self.width + (x + dx)
                if self.maze_map[cell] != 0:
                    return False

        return True

    def prep_maze_str(self) -> str:
        """Serialize the maze map into a binary string.

        Returns:
            String where each cell is represented by 4 bits.
        """
        maze_str: str = ""
        for cell in self.maze_map:
            maze_str += format(cell, '04b')
        return maze_str

    def put_42(self) -> None:
        """Mark a fixed "42" pattern area in the center of the maze.

        Cells in this pattern are preserved and excluded from generation steps.
        """
        x = self.width // 2
        y = self.height // 2

        center = y * self.width + x

        self.pattern.add(center - 1)
        self.pattern.add(center - 2)
        self.pattern.add(center - 3)
        self.pattern.add(center - 3 - self.width)
        self.pattern.add(center - 3 - self.width * 2)
        self.pattern.add(center - 1 + self.width)
        self.pattern.add(center - 1 + self.width * 2)

        self.pattern.add(center + 1)
        self.pattern.add(center + 2)
        self.pattern.add(center + 3)
        self.pattern.add(center + 1 + self.width)
        self.pattern.add(center + 1 + self.width * 2)
        self.pattern.add(center + 2 + self.width * 2)
        self.pattern.add(center + 3 + self.width * 2)
        self.pattern.add(center + 3 - self.width)
        self.pattern.add(center + 3 - self.width * 2)
        self.pattern.add(center + 2 - self.width * 2)
        self.pattern.add(center + 1 - self.width * 2)

    def print_maze(self) -> None:
        """Print the current numeric maze map to stdout for debugging."""
        for y in range(self.height):
            for x in range(self.width):
                index = y * self.width + x
                print(f"{self.maze_map[index]:2}", end=" ")
            print()

    def save_output(self, file_name: str) -> None:
        """Save maze map and entry/exit coordinates to output_test.txt."""
        with open(file_name, "w") as file:
            for y in range(self.height):
                for x in range(self.width):
                    cell = self.maze_map[y * self.width + x]
                    hexa = str(hex(cell))[2:].capitalize()
                    file.write(hexa)
                file.write("\n")
            entry_x = self.entry % self.width
            entry_y = self.entry // self.width
            exit_x = self.exit % self.width
            exit_y = self.exit // self.width
            file.write("\n")
            file.write(f"{entry_x},{entry_y}\n")
            file.write(f"{exit_x},{exit_y}\n")

    def wilson(self) -> None:
        """Generate maze corridors using Wilson's algorithm.

        Starts from the entry point and repeatedly performs loop-erased random
        walks from unvisited cells until all non-pattern cells are connected.
        """
        self.remaining.discard(self.exit)
        start = self.entry
        self.clear_42_pattern()
        path = self.random_walk(start)
        for i in range(len(path) - 1):
            self.trim_wall(path[i], path[i + 1])
            self.remaining.discard(path[i])
        self.remaining.discard(path[-1])

        while self.remaining:
            start = self.maze_random.choice(list(self.remaining))
            path = self.random_walk(start)
            for i in range(len(path) - 1):
                self.trim_wall(path[i], path[i + 1])
                self.remaining.discard(path[i])

            self.remaining.discard(path[-1])

    def random_walk(self, start: int) -> List[int]:
        """Run a random walk until it reaches the carved region.

        During the walk, loops are removed to keep the path simple.

        Args:
            start: Starting cell index.

        Returns:
            Loop-erased path of visited cell indices.
        """
        current_cell = start

        path = list()
        path.append(start)
        while current_cell in self.remaining:
            choosen_neighbor = self.chose_neighbor(current_cell)
            if choosen_neighbor in path:
                self.enrase_loop(path, choosen_neighbor)
            else:
                path.append(choosen_neighbor)
            current_cell = choosen_neighbor
        return path

    def clear_42_pattern(self) -> None:
        """Remove all reserved pattern cells from the unvisited set."""
        for cell in self.pattern:
            self.remaining.discard(cell)

    def enrase_loop(self, path: List[int], cell: int) -> None:
        """Erase a loop in the current path starting after the repeated cell.

        Args:
            path: Current random-walk path.
            cell: Cell that appears earlier in the path and closes a loop.
        """
        loop_start = path.index(cell)
        del path[loop_start + 1:]

    def chose_neighbor(self, cell: int) -> int:
        """Choose a random valid neighboring cell outside the pattern.

        Args:
            cell: Current cell index.

        Returns:
            Index of a randomly selected neighboring cell.
        """
        x = cell % self.width
        y = cell // self.width

        neighbors = []

        if y > 0 and cell - self.width not in self.pattern:
            neighbors.append(cell - self.width)

        if y < self.height - 1 and cell + self.width not in self.pattern:
            neighbors.append(cell + self.width)

        if x > 0 and cell - 1 not in self.pattern:
            neighbors.append(cell - 1)

        if x < self.width - 1 and cell + 1 not in self.pattern:
            neighbors.append(cell + 1)

        return self.maze_random.choice(neighbors)

    def trim_wall(self, cell: int, neighbor: int) -> None:
        """Remove the wall between two adjacent cells.

        Args:
            cell: Source cell index.
            neighbor: Adjacent cell index.

        Raises:
            ValueError: If the provided cells are not direct neighbors.
        """
        if neighbor == cell + 1:  # prawo
            self.maze_map[cell] &= ~0b0010
            self.maze_map[neighbor] &= ~0b1000

        elif neighbor == cell - 1:  # lewo
            self.maze_map[cell] &= ~0b1000
            self.maze_map[neighbor] &= ~0b0010

        elif neighbor == cell + self.width:  # dół
            self.maze_map[cell] &= ~0b0100
            self.maze_map[neighbor] &= ~0b0001

        elif neighbor == cell - self.width:  # góra
            self.maze_map[cell] &= ~0b0001
            self.maze_map[neighbor] &= ~0b0100
        else:
            raise ValueError(f"{cell} and {neighbor} are not neighbors")


if __name__ == "__main__":
    maze_gen = MazeGenerator()
    maze = Maze(150, 150, (0, 0), (99, 99), True)
    print(len(maze_gen.cerate_maze(maze, "test.txt", 1)))
