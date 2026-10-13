*This project has been created as part of the 42 curriculum by atchioue, ymouafak*

# Description

**Pac-Man** is a 2D maze game developed in Python using the Pygame library. The goal of the project is to recreate the classic Pac-Man gameplay, where the player navigates through a maze, collects gums, avoids ghosts, and progresses through levels.

The project implements player movement and animation, collision detection with maze walls, ghost behavior, and a scoring system. It also includes super gums that activate a special mode, allowing the player to interact with ghosts differently for a limited time.

The game is structured using object-oriented programming, with separate components responsible for game logic, player and ghost behavior, maze management, and rendering.

# Instructions
The project ships with a `Makefile` that wraps the common tasks:

| Command | What it does |
|---|---|
| `make install` | Installs the project's Python dependencies. |
| `make run` |  Execute the main script of the project|
| `make debug` | Runs the simulation under Python's built-in debugger (`pdb`). |
| `make lint` | Runs `flake8` and `mypy` with the required flags. |
| `make lint-strict` | Runs `flake8` and `mypy --strict`. |
| `make clean` | Removes `__pycache__` and `.mypy_cache`. |

# Resources

# Configuration
The config file based on the next keys that you should provide through i json file and a backup to default values when missed values or forgot to add thos keys, and ignore any other key not used in our structure
  | key | used for what |
|---|---|
| `heart` | the total lives you have during the game |
| `current_score` |  the score you collect during the game from eating gums, ghosts...|
| `points_per_gum` | the value added to your score after eating normal gum |
| `points_per_super_gum` | the value added to your score after eating super gum |
| `points_per_ghost` | the value added to your score after eating a ghost |
| `cheat_mode` | a boolean to set when activate or deactivate the cheat mode |
| `livel_time` | the remaining time for this level to complete it  |
| `level` | the level you in right now |


# Highscore

The game implements a persistent highscore system using a local JSON file (`scores.json`). This allows player scores to be preserved between game sessions without requiring an external database or an internet connection.

When a player loses the game or completes all levels, the Game Over or Victory screen displays their final score and prompts them to enter a name before saving it.

The highscore system is managed through the `DataBase` class, which handles loading, saving, and sorting scores. The scoreboard displays the top 10 scores in descending order.

The system follows these validation rules:

- Player names must contain at most 10 characters, using alphanumeric characters and spaces only.
- Scores must be non-negative integers.
- Missing or corrupted JSON files must not cause the game to crash.
- Invalid records are ignored while valid records are preserved whenever possible.

**Why this approach?**

JSON was chosen because it is lightweight, human-readable, and directly supported by Python through the built-in `json` module. Since this is a local arcade game with a small number of highscore entries, a more complex database system was unnecessary.

# Maze Generation
to extract mazegenerator-2.1.0-py3-none-any.whl

To extract the contents of mazegenerator-2.1.0-py3-none-any.whl, you can use the unzip command, as a Wheel file is essentially a ZIP archive 

`unzip mazegenerator-2.1.0-py3-none-any.whl -d <destination_folder>`

better methode is, that you can install it directly into your Python environment using pip, which handles the extraction and installation automatically:

`pip install mazegenerator-2.1.0-py3-none-any.whl`


If you are using uv, you can install it with:

`uv pip install mazegenerator-2.1.0-py3-none-any.whl`

the then you just import that class inside the pakage to you main.py when need it as:

`from mazegenerator.mazegenerator import MazeGenerator`

then to use it you can create obj of this class and the maze while be builded at the same time:

`maze_engine = MazeGenerator(size=(20, 20), seed=42)`

and this obj have the attribute maze where the 2D array representation stored

`maze = maze_engine.maze`

# Implementation
the implementation based on this main elements:

- **Structure:** one module per concern: `adapter.py` (coordinates, gums), `moves.py` (movement), `ghosts.py` (AI), `drawing.py` (rendering, Pac-Man moves, collisions), plus `cell.py`, `pacman_player.py` and `ghost_maker.py`.
- **Maze:** a 2-D list (`maze[y][x]`) of 4-bit wall masks (`1` upper, `2` right, `4` lower, `8` left), so a wall test is one bitwise AND. `15` is a fully closed cell (drawn as a block, no gum).
- **Coordinates:** the grid `(x, y)` and the window (pixel center of each cell) are linked by `Adapter.calculat_point` and two dictionaries, `window_to_grad` and `grad_to_window`, for O(1) conversion. An entity is "on a cell" when its pixel position is a key of `window_to_grad`.
- **Movement:** logic is grid-based, display is continuous. Each entity's `Move` holds a target cell center; every frame `Move.next_frame` advances by `speed * dt` and clamps at the target, so speed does not depend on the frame rate.
- **Walls and collisions:** a move is allowed only if the source cell has no wall on the side of travel and the destination has none on the opposite side (`Drawing.cheeck_colistion`, `Ghost.check_wall`). Pac-Man and a ghost collide when their pixel distance is below 40 px.
- **Gums:** one per cell center, about half removed at random; the four corners always keep theirs and become super-gums. A gum is eaten when Pac-Man's position equals its position.
- **Ghosts:** on each cell center, a ghost scores its reachable neighbors (not the cell it came from, unless dead end) with a breadth-first search to Pac-Man, then picks the shortest path (normal ghost), a random neighbor (other types), or a random neighbor that does not get closer and is not in `visited_cells` (edible ghost). That is at most four BFS runs per decision, each linear in the number of cells.
# General Software Architecture
https://www.tldraw.com/f/_qoGUTOY1yO6m9fBaGKOA?d=v-2857.-1843.10698.6699.page

# Packaging

The game is packaged using **PyInstaller**, which bundles the Python interpreter, required libraries, game modules, and graphical assets into a standalone application.

This allows players to launch the game without manually installing Python, Pygame, or the MazeGenerator package.

The packaging process includes the required assets from the `menu_images`, `ghosts_images`, and `images` directories.

To ensure compatibility between normal Python execution and the packaged application, a `PathResolver` utility resolves resource paths depending on the execution environment.

The PyInstaller configuration is stored in `Pacman.spec` at the repository root, allowing the application to be rebuilt using:

```bash
uv run pyinstaller --clean --noconfirm Pacman.spec
```

The resulting application is generated inside the `dist/` directory.

**Why PyInstaller?**

PyInstaller was chosen because it supports Python and Pygame applications, automatically collects imported Python dependencies, and provides reproducible builds through its specification file.

# Project Management

The project was developed collaboratively by two team members using **Git, GitHub, and GitHub Projects**.

We adopted a Kanban-based workflow to organize development tasks, assign responsibilities, and track progress through different stages, including Backlog, Ready, In Progress, In Review, and Done.

GitHub Issues were used to describe individual features and development tasks, while Git commits provided a record of implementation progress, bug fixes, and contributions from each team member.

The work was divided across several areas, including maze rendering, player movement, ghost behavior, game logic, user interface development, highscores, and packaging.

A dedicated directory contains additional information about team organization, development progress, technical decisions, challenges, and supporting evidence.

**Detailed documentation:** [Project Management](project_management/README.md)