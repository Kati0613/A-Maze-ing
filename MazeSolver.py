from typing import List
from Maze import Maze
from MazeGenerator import MazeGenerator
from collections import deque


class MazeSolver:
    def prepere_data(self, maze: Maze):
        self.maze_map = maze.map
        self.width = maze.width
        self.height = maze.height
        self.entry = maze.entry[1] * self.width + maze.entry[0]
        self.exit = maze.exit[1] * self.width + maze.exit[0]
        self.queue = deque()
        self.visited = set()
        self.came_from = {}

    def solve_maze(self, maze: Maze):
        self.prepere_data(maze)
        self.queue.append(self.entry)
        self.visited.add(self.entry)

        while self.queue:
            current = self.queue.popleft()
            if current == self.exit:
                break
            neighbors = self.check_neighbors(current)
            #print("currnet: ", current, "neighbors: ", neighbors)
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
        #self.save_output("dupa", path)
        return self.prepere_output(path)
    
    def solve_maze_steps(self, maze: Maze):
        self.prepere_data(maze)
        self.queue.append(self.entry)
        self.visited.add(self.entry)

        while self.queue:
            current = self.queue.popleft()
            visited_new = []
            #yield [(cell % self.width, cell // self.width) for cell in self.visited]
            #print([(cell % self.width, cell // self.width) for cell in self.visited])
            if current == self.exit:
                break
            neighbors = self.check_neighbors(current)
            #print("currnet: ", current, "neighbors: ", neighbors)
            for n in neighbors:
                if n not in self.visited:
                    self.visited.add(n)
                    visited_new.append((n % self.width, n // self.width))
                    self.queue.append(n)
                    self.came_from[n] = current
            yield(visited_new)
            #print("new: ", visited_new)
        
        path = []
        current = self.exit

        while current != self.entry:
            path.append(current)
            current = self.came_from[current]

        path.append(self.entry)
        path.reverse()
        #self.save_output("dupa", path)
        return self.prepere_output(path)

    def prepere_output(self, path: List):
        output = []
        for cell in path:
            output.append((cell % self.width, cell // self.width))
        
        return output

    def save_output(self, file_name: str, path: List):
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
        
        print(output)

        with open(file_name, "a") as file:
            file.write(output)

    def check_neighbors(self, current: int):
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
    print(gen.cerate_maze(maze, 1))

    # gen = solver.solve_maze_steps(maze)
    # print(next(gen))  # krok 1
    # print(next(gen))  # krok 2
    # print(next(gen))  # krok 3

    for step in solver.solve_maze_steps(maze):
          print(step)
    
    print(solver.solve_maze_steps(maze))