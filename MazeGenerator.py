from random import Random
from typing import List, Union, Set, Generator, Optional, Tuple

class MazeGenerator:
    def __init__(self, seed: int, width: int, height: int, is_perfect: bool, entry: int, exit: int) -> None:
        self.maze_random = Random()
        self.maze_random.seed(seed)
        self.maze_map: List[Union[bool, int]] = [0xF] * (width * height)
        self.width = width
        self.height = height
        self.remaining: Set[int] = set(range(self.width * self.height))
        self.seed = seed
        self.is_perfect = is_perfect
        self.entry = entry
        self.exit = exit
        self.pattern: Set[int] = set()


    def put_42(self):
        x = self.width // 2
        y = self.height // 2

        center = y * self.width + x

        self.pattern.add(center - 1)
        self.pattern.add(center - 2)
        self.pattern.add(center - 3)
        self.pattern.add(center - 3 - self.width)
        self.pattern.add(center - 3 - self.width * 2)
        #self.pattern.add(center - 3 - self.width * 3)
        self.pattern.add(center - 1 + self.width)
        self.pattern.add(center - 1 + self.width * 2)
        #self.pattern.add(center - 1 + self.width * 3)

        self.pattern.add(center + 1)
        self.pattern.add(center + 2)
        self.pattern.add(center + 3)
        self.pattern.add(center + 1 + self.width)
        #self.pattern.add(center + 1 + self.width * 2)
        self.pattern.add(center + 1 + self.width * 2)
        self.pattern.add(center + 2 + self.width * 2)
        self.pattern.add(center + 3 + self.width * 2)
        #self.pattern.add(center + 3 - self.width * 2)
        self.pattern.add(center + 3 - self.width)
        self.pattern.add(center + 3 - self.width * 2)
        self.pattern.add(center + 2 - self.width * 2)
        self.pattern.add(center + 1 - self.width * 2)

    def print_maze(self):
        for y in range(self.height):
            for x in range(self.width):
                index = y * self.width + x
                print(f"{self.maze_map[index]:2}", end=" ")
            print()


    def save_output(self) -> None:
        with open("output_test.txt", "w") as file:
            for y in range(self.height):
                for x in range(self.width):
                    hexa = str(hex(self.maze_map[y * self.width + x]))[2:].capitalize()
                    file.write(hexa)
                file.write("\n")
            entry_x = self.entry % self.width
            entry_y = self.entry // self.width
            exit_x = self.exit % self.width
            exit_y = self.exit // self.width
            file.write("\n")
            file.write(f"{entry_x},{entry_y}\n")
            file.write(f"{exit_x},{exit_y}\n")
            file.write("dupa")

    def wilson(self):
        self.remaining.discard(self.exit)
        start = self.entry
        self.clear_42_pattern()
        #self.remaining.remove(start)
        path = self.random_walk(start)
        print("full path: ", path)
        for i in range(len(path) - 1):
            self.trim_wall(path[i], path[i + 1])
            self.remaining.discard(path[i])
        self.remaining.discard(path[-1])
        print("remaining: ", self.remaining)
        while self.remaining:
            start = self.maze_random.choice(list(self.remaining))
            path = self.random_walk(start)
            print("full path: ", path)
            for i in range(len(path) - 1):
                self.trim_wall(path[i], path[i + 1])
                self.remaining.discard(path[i])

            self.remaining.discard(path[-1])
        self.print_maze()
        print(self.remaining)
    
    def random_walk(self, start: int):
        current_cell = start
        
        path = list()
        path.append(start)
        while current_cell in self.remaining:
            choosen_neighbor = self.chose_neighbor(current_cell)
            #print(choosen_neighbor)
            if choosen_neighbor in path:
                #print("looooop")
                self.enrase_loop(path, choosen_neighbor)
            else:
                path.append(choosen_neighbor)
            current_cell = choosen_neighbor
            #print("new somsiad: ", choosen_neighbor)
        #print(path)
        return path

    def clear_42_pattern(self) -> None:
        for cell in self.pattern:
            self.remaining.discard(cell)

    def enrase_loop(self, path: List[int], cell: int) -> None:
        #print(path)
        #print(cell)
        loop_start = path.index(cell)
        #for cell in path[loop_start:]:
            #self.remaining.add(cell)
        #print(self.remaining)
        del path[loop_start + 1:]


    def chose_neighbor(self, cell: int) -> int:
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
    maze = MazeGenerator(3, 21, 21, True, 0, 440)
    maze.put_42()
    maze.print_maze()
    maze.wilson()
    maze.save_output()
