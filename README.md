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

# Project Management