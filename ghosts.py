
from collections import deque
import random


class Ghost:

    def __init__(self, spawn_point, image, type, maze, player_pos, speed) -> None:
        self.spawn_point = spawn_point
        self.image = image
        self.current_coords = spawn_point
        self.previous_cell = spawn_point
        self.type = type
        self.maze = maze
        self.player_pos = player_pos
        self.edible = False
        self.visited_cells = set()
        self.speed = speed

    def check_wall(self, direction, starting_cell, next_cell):
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

    def get_valid_neighbors(self, x, y):
        neighbors = []

        # what changed:
        # coordinates are (x, y)
        # maze is accessed using [y][x]
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

    def bfs(self, starting_point, target_point):
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

    def next_cell(self, starting_point, goal_point):
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
