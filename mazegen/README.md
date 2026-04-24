# mazegen

A lightweight library for generating and solving mazes.

The package exposes three main classes:
- `Maze` - maze data model (dimensions, entry/exit, wall map)
- `MazeGenerator` - Wilson algorithm based generator
- `MazeSolver` - BFS solver that returns the shortest path

## Installation

Requirements:
- Python 3.6+

From the project root directory:

```bash
# Install using wheel
pip install mazegen-1.0.0-py3-none-any.whl

# Or install using source distribution
pip install mazegen-1.0.0.tar.gz
```

## Usage

```python
from mazegen import Maze, MazeGenerator, MazeSolver

maze = Maze(
    width=20,
    height=15,
    entry=(0, 0),
    exit=(19, 14),
    is_perfect=True,
)

generator = MazeGenerator()
bitstring = generator.cerate_maze(maze, seed=42)

solver = MazeSolver()
path = solver.solve_maze(maze)

print("Bitstring length:", len(bitstring))
print("Path length:", len(path))
print("First steps:", path[:5])
```

## Parameters

### `Maze(width, height, entry, exit, is_perfect)`

Maze data model.

Parameters:
- `width: int` - width in cells
- `height: int` - height in cells
- `entry: tuple[int, int]` - start coordinate `(x, y)`
- `exit: tuple[int, int]` - end coordinate `(x, y)`
- `is_perfect: bool` - whether the maze should be perfect (no loops)

### `MazeGenerator.cerate_maze(maze, seed=None)`

Parameters:
- `maze: Maze` - maze configuration object to populate
- `seed: int | None` - optional random seed used for deterministic output

### `MazeSolver.solve_maze(maze)`

Parameters:
- `maze: Maze` - maze instance with `map` already filled by the generator

### `MazeSolver.solve_maze_steps(maze)`

Parameters:
- `maze: Maze` - maze instance with `map` already filled by the generator

## Structure Access

Important fields after generation:
- `map: list[int]` - wall map for each cell
- `start`, `end` - linear indices of entry/exit cells

Cell wall bits:
- `0b0001` - top
- `0b0010` - right
- `0b0100` - bottom
- `0b1000` - left

A set bit means that a wall exists.

## API Reference

### `MazeGenerator`

Methods:
- `cerate_maze(maze, seed=None) -> str`
  - generates the maze
  - fills `maze.map`
  - returns a bitstring: concatenation of 4-bit wall representations

Note:
- The method name is currently `cerate_maze` (the typo is kept for compatibility with the current code).

### `MazeSolver`

Methods:
- `solve_maze(maze) -> list[tuple[int, int]]`
  - returns the shortest path from entry to exit
- `solve_maze_steps(maze) -> iterator[list[tuple[int, int]]]`
  - returns incremental BFS steps (useful for animation)

## Limitations

- Entry and exit must be inside maze bounds.
- The current implementation writes an additional helper file `output_test.txt` during generation.

## Authors

- Zuzanna Gorecka
- Katarzyna Kulagowska
