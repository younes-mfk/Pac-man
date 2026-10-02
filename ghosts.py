
from collections import deque
import random


class Ghost:

    def __init__(self, spawn_point, image, type) -> None:
        self.spawn_point = spawn_point
        self.image = image
        self.current_coords = spawn_point
        self.previous_cell = spawn_point
        self.type = type
        self.visited_cells = set()

    def check_wall(self, direction, maze, starting_cell, next_cell):
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

    def get_valid_neighbors(self, maze, x, y):
        neighbors = []
        current_cell = maze[x][y]

        if x > 0 and self.check_wall("up", maze, current_cell, maze[x - 1][y]):
            neighbors.append((x - 1, y))

        if y > 0 and self.check_wall("left", maze, current_cell,
                                     maze[x][y - 1]):
            neighbors.append((x, y - 1))

        if y < len(maze[0]) - 1 and self.check_wall("right", maze,
                                                    current_cell,
                                                    maze[x][y + 1]):
            neighbors.append((x, y + 1))

        if x < len(maze) - 1 and self.check_wall(
            "down", maze, current_cell, maze[x + 1][y]
        ):
            neighbors.append((x + 1, y))

        return neighbors

    def bfs(self, maze, starting_point, target_point):
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

            neighbors = self.get_valid_neighbors(maze, cell_x, cell_y)
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.append(neighbor)
                    parent[neighbor] = (cell_x, cell_y)

        return float('inf')

    def next_cell(self, maze, starting_point, goal_point,  edible=True):
        neighbors = self.get_valid_neighbors(maze, starting_point[0], starting_point[1])
        unvisited_neighbors = [neighbor for neighbor in neighbors
                               if neighbor != self.previous_cell]

        if not unvisited_neighbors:
            unvisited_neighbors = neighbors

        roads = [(neighbor, self.bfs(maze, neighbor, goal_point)) for neighbor in unvisited_neighbors]

        if not roads:
            return starting_point

        if not edible:

            if self.type == "normal":
                to_cell = min(roads, key=lambda x: x[1])

            else:
                to_cell = random.choice(roads)

        else:
            current_distance = self.bfs(maze, starting_point, goal_point)
            valid_ones = [road for road in roads
                          if road[1] >= current_distance or
                          road[0] not in self.visited_cells]
            if valid_ones:
                to_cell = random.choice(valid_ones)
            else:
                self.visited_cells.clear()
                to_cell = random.choice(roads)
            self.visited_cells.add(to_cell[0])

        self.previous_cell = starting_point
        return to_cell[0]
