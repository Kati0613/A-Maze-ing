*This project has been created as part of the 42 curriculum by kkulagow, zgorecka.*

# A-Maze-ing

## Description
Implementation of a maze generator in Python that takes a configuration file, generates a maze, possibly perfect (with a single path between entrance and exit), and writes it to a file using a hexadecimal wall representation. It also provide a visual representation using MLX library of the maze and organize code so that the generation logic can be reused later

## Config structure
The configuration file defines how the maze is generated.  
It follows a simple `KEY=VALUE` format, with one setting per line.

### Format rules
- Each line must contain exactly one `KEY=VALUE` pair
- Lines starting with `#` are treated as comments and ignored
- Keys are case-sensitive
- Extra whitespace should be avoided for consistency

### Required keys

| Key         | Description                          | Example            |
|------------|--------------------------------------|--------------------|
| WIDTH       | Maze width (number of cells)         | WIDTH=20           |
| HEIGHT      | Maze height (number of cells)        | HEIGHT=15          |
| ENTRY       | Entry coordinates (x,y)              | ENTRY=0,0          |
| EXIT        | Exit coordinates (x,y)               | EXIT=19,14         |
| OUTPUT_FILE | Output filename                      | OUTPUT_FILE=maze.txt |
| PERFECT     | Whether the maze is perfect (True/False) | PERFECT=True   |

### Example configuration

```ini
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

## Maze generation algorithm

## Algorithm choice

## Reusable part

## Display Options
The project provides a graphical visualization of the maze using MiniLibX (MLX), allowing the user to interact with the generated maze in real time.
The visual representation displays:
- maze walls
- entry point
- exit point
- shortest valid path
- the visible "42" pattern made of fully closed cells

Available interactions
The user can perform the following actions:

- generate a new random maze with width and height displayed on screen
- show or hide the shortest valid path
- change of size
- change of width and height
- apply specific colours to  highlight the "42" pattern
- apply colours to maze
- easter egg


During generation, cells are temporarily filled with random colours to visualize how the maze is being created.
After generation is completed, the temporary colours are cleared and the final shortest path can be shown separately.

## Team and project management

### Team roles 
Backend developer - Zuzanna Gorecka

Frontend developer - Katarzyna Kulagowska

### Planning and evolution
At the beginning, we planned a strict separation between frontend and backend with a simple API-based communication model. We also defined a basic milestone structure: configuration parsing → maze generation → visualization → final integration.

As the project evolved, we adapted our approach:
- We simplified communication between front-end and back-end to speed up development.
- Some features were added as some like maze animated generation were postponed for future development.

### What worked well
- Clear division of responsibilities within the team
- Regular integration between frontend and backend
- Early focus on a working prototype
- Flexibility in adapting the plan when issues appeared

### What could be improved
- better time management resulting in quicker evaluation
- early decided method of data transform from back-end to front-end

### Tools used
- **MLX** – used for frontend development and UI implementation
- Git & GitHub – version control and collaboration
- Communication tools (Messenger) – team coordination
- Visual Studio Code

## Instructions
The project uses a Makefile to simplify common development tasks such as environment setup, running the application, building the package, code quality checks, and cleaning the project.

- **install** – creates a Python virtual environment and installs all required dependencies, including development tools and optional packages from `requirements.txt` if available.

- **run** – executes the main application using the default configuration file and generates the maze output.

- **debug** – starts the application in debugging mode using Python’s built-in debugger, allowing step-by-step execution.

- **build** – builds the project into distributable formats (wheel and source archive), preparing it for distribution or reuse.

- **lint** – runs static code analysis tools to check code style and type correctness.

- **clean** – removes all generated files, including the virtual environment, caches, and build artifacts, restoring the project to a clean state.

## Resources
AI was used as a supporting tool during the development of the project, mainly for improving code quality and documentation.