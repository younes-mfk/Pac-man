"""Define the Ghost class: maze navigation and pathfinding for ghosts."""

from collections import deque
from moves import Move
import random
from typing import Set, Tuple, Any
import pygame


class Ghost:
    """Represent a ghost that moves through the maze toward a goal.

    The ghost uses breadth-first search (BFS) to choose its next cell
    Its behavior depends on its type and on whether it is edible
    """

    def __init__(self, spawn_point: Tuple, image: pygame.surface.Surface,
                 type: str, maze: list[list],
                 player_pos: Tuple,
                 speed: int) -> None:
        """Initialize the ghost.

        Args:
            spawn_point (Tuple): (x, y) cell where the ghost spawns.
            image (pygame.surface.Surface): Image used to draw the
                ghost.
            type (str): Ghost type, e.g. "normal" for a chasing ghost.
            maze (list[list]): Maze grid where each cell is an integer
                whose bits encode its walls.
            player_pos (Tuple): Position of the player.
            speed (int): Movement speed of the ghost.

        Returns:
            None.
        """

        self.spawn_point = spawn_point
        self.image = image
        self.current_coords = spawn_point
        self.previous_cell = spawn_point
        self.type = type
        self.maze = maze
        self.player_pos = player_pos
        self.edible = False
        self.visited_cells: Set = set()
        self.speed = speed
        self.move: Move
        self.respawning_time = 0

    def check_wall(self, direction: str, starting_cell: int,
                   next_cell: int) -> int:
        """Check whether movement between two adjacent cells is open.

        Each cell is an integer whose lowest four bits are walls:
        0b0001 north, 0b0010 east, 0b0100 south, 0b1000 west. Movement
        is blocked if either cell has a wall on the shared side.

        Args:
            direction (str): Direction of travel: "right", "left",
                "up", or "down".
            starting_cell (int): Wall bits of the cell being left.
            next_cell (int): Wall bits of the cell being entered.

        Returns:
            int: 0 if a wall blocks the move, 1 if the way is open.
        """
        from_cell = starting_cell
        to_cell = next_cell
        if direction == "right":
            if (from_cell & 0B00000010) or (to_cell & 0B00001000):
                return 0
        elif direction == "left":
            if from_cell & 0B00001000 or to_cell & 0B00000010:
                return 0
        elif direction == "up":
            if from_cell & 0B00000001 or to_cell & 0B00000100:
                return 0
        elif direction == "down":
            if from_cell & 0B00000100 or to_cell & 0B00000001:
                return 0
        return 1

    def get_valid_neighbors(self, x: int, y: int) -> list:
        """Find the cells reachable in one step from a given cell.

        Only the four orthogonal neighbors inside the maze bounds are
        considered, and those separated by a wall are excluded.

        Args:
            x (int): Column of the cell.
            y (int): Row of the cell.

        Returns:
            list: (x, y) tuples of the neighboring cells that can be
                entered from (x, y).
        """
        neighbors = []

        current_cell = self.maze[y][x]

        if y > 0:
            next_cell = self.maze[y - 1][x]

            if self.check_wall("up", current_cell, next_cell):
                neighbors.append((x, y - 1))

        if x > 0:
            next_cell = self.maze[y][x - 1]

            if self.check_wall("left", current_cell, next_cell):
                neighbors.append((x - 1, y))

        if x < len(self.maze[0]) - 1:
            next_cell = self.maze[y][x + 1]
            if self.check_wall("right", current_cell, next_cell):
                neighbors.append((x + 1, y))

        if y < len(self.maze) - 1:
            next_cell = self.maze[y + 1][x]

            if self.check_wall("down", current_cell, next_cell):
                neighbors.append((x, y + 1))

        return neighbors

    def bfs(self, starting_point: Tuple,
            target_point: Tuple) -> int | float:
        """Measure the shortest path between two cells using BFS.

        Args:
            starting_point (Tuple): (x, y) cell where the search starts.
            target_point (Tuple): (x, y) cell to reach.

        Returns:
            int | float: Number of cells on the shortest path,
                including both the start and the target, or
                float("inf") if the target cannot be reached.
        """
        goal_x, goal_y = target_point
        queue = deque([starting_point])
        visited = [starting_point]
        parent: dict = {starting_point: None}
        path = []

        while queue:
            cell_x, cell_y = queue.popleft()
            if cell_x == goal_x and cell_y == goal_y:
                current = (cell_x, cell_y)
                while current:
                    path.append(current)
                    current = parent[current]

                return len(path)

            neighbors = self.get_valid_neighbors(cell_x, cell_y)
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.append(neighbor)
                    parent[neighbor] = (cell_x, cell_y)

        return float('inf')

    def next_cell(self, starting_point: Tuple, goal_point: Tuple) -> Any:
        """Choose the next cell the ghost should move to.

        Turning back to the previous cell is avoided unless it is the
        only option. The choice depends on the ghost's state:

        * Not edible and type "normal": the neighbor with the shortest
          BFS distance to the goal (chases the goal).
        * Not edible and any other type: a random neighbor.
        * Edible: a random neighbor that is not closer to the goal than
          the current cell and has not been visited recently; if none
          qualifies, the visited set is reset and any neighbor is
          picked at random.

        Args:
            starting_point (Tuple): (x, y) cell the ghost is in.
            goal_point (Tuple): (x, y) cell the ghost is heading to
                (or fleeing from when edible).

        Returns:
            Any: (x, y) of the chosen neighbor cell, or starting_point
                if there is no neighbor to move to.
        """
        neighbors = self.get_valid_neighbors(starting_point[0],
                                             starting_point[1])
        unvisited_neighbors = [neighbor for neighbor in neighbors
                               if neighbor != self.previous_cell]

        if not unvisited_neighbors:
            unvisited_neighbors = neighbors

        roads = [(neighbor, self.bfs(neighbor, goal_point))
                 for neighbor in unvisited_neighbors]

        if not roads:
            return starting_point

        if not self.edible:

            if self.type == "normal":
                to_cell = min(roads, key=lambda x: x[1])

            else:
                to_cell = random.choice(roads)

        else:
            current_distance = self.bfs(starting_point, goal_point)
            valid_ones = [road for road in roads
                          if road[1] >= current_distance and
                          road[0] not in self.visited_cells]
            if valid_ones:
                to_cell = random.choice(valid_ones)
            else:
                self.visited_cells.clear()
                to_cell = random.choice(roads)
            self.visited_cells.add(to_cell[0])

        self.previous_cell = starting_point
        return to_cell[0]
