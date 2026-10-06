from cell import CellDimention


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

        (self.gums_positions, self.window_to_grad,
         self.super_gums_positions) = self.get_gums_positions(maze)

        self.grad_to_window = {value: key
                               for key, value in self.window_to_grad.items()}
        self.spawn_corners = self.super_gums_positions

    def get_gums_positions(self, maze):
        positions_super_gums = []
        positions_gums = []
        window_to_grad = {}
        for y in range(len(maze)):
            for x in range(len(maze[0])):
                # node = maze[y][x]
                positions_gums.append(((self.start_drawing_point[0] + (self.cell_dimontions.width * (x)) + self.cell_dimontions.width // 2),
                                      (self.start_drawing_point[1] + (self.cell_dimontions.height * (y)) + self.cell_dimontions.height // 2)))
                window_to_grad[positions_gums[-1]] = (x, y)
                # window_to_grad ====> center of cell postion to grid[y][x]
                if (y == 0 or y == len(maze) - 1) and (x == 0 or x == len(maze[0]) - 1):
                    positions_super_gums.append((x, y))

        return positions_gums, window_to_grad, positions_super_gums
