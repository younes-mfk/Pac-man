from cell import CellDimention
import random


class Adapter:
    #  this class to make calculs dynamic and varie
    #  with the variation of maze and window dimentions you put
    def __init__(self, maze, window_dimention=(2600, 2000)):

        self.maze = maze

        self.cell_dimontions = CellDimention

        self.window_dimentions = window_dimention

        self.maze_dimentions = ((len(maze[0]) * self.cell_dimontions.width),
                                (len(maze) * self.cell_dimontions.height))

        self.start_drawing_point = (
            (self.window_dimentions[0] // 2) - (self.maze_dimentions[0]//2),
            (self.window_dimentions[1] // 2) - (self.maze_dimentions[1]//2))

        if len(maze[0]) % 2 == 0:
            self.player_position_x = (self.start_drawing_point[0] +
                                      (self.maze_dimentions[0] // 2) -
                                      self.cell_dimontions.width // 2)

        else:
            self.player_position_x = (self.start_drawing_point[0] +
                                      self.maze_dimentions[0] // 2)

        if len(maze) % 2 == 0:
            self.player_position_y = (self.start_drawing_point[1] +
                                      (self.maze_dimentions[1] // 2) -
                                      self.cell_dimontions.height // 2)

        else:
            self.player_position_y = (self.start_drawing_point[1] +
                                      (self.maze_dimentions[1] // 2))

        self.player_position = (self.player_position_x, self.player_position_y)

        (self.gums_positions, self.super_gums_positions,
         self.window_to_grad) = self.get_gums_positions(maze)

        self.grad_to_window = {value: key
                               for key, value in self.window_to_grad.items()}
        self.spawn_corners = self.super_gums_positions.copy()

    def calculat_point(self, start_drawing, cell, x, y):
        return ((start_drawing[0] + (cell.width * (x)) + cell.width // 2),
                (start_drawing[1] + (cell.height * (y)) + cell.height // 2))

    def get_gums_positions(self, maze):
        positions_super_gums = []
        positions_gums = []
        window_to_grad = {}
        for y in range(len(maze)):
            for x in range(len(maze[0])):
                positions_gums.append(
                    self.calculat_point(self.start_drawing_point,
                                        self.cell_dimontions, x, y))
                window_to_grad[positions_gums[-1]] = (x, y)
                # window_to_grad ====> (center of cell postion) to (grid[y][x])
                # remember (center of cell not corner of cell)
                if ((y == 0 or y == len(maze) - 1) and
                   (x == 0 or x == len(maze[0]) - 1)):
                    positions_super_gums.append((x, y))

        random.shuffle(positions_gums)
        for i in range(len(positions_gums)//2):
            if window_to_grad[positions_gums[i]] not in positions_super_gums:
                positions_gums.remove(positions_gums[i])

        return positions_gums, positions_super_gums, window_to_grad
