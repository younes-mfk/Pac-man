from mazegenerator.mazegenerator import MazeGenerator
import pygame


class Cell:
    def __init__(self):
        self.upper_wall = 0
        self.right_wall = 0
        self.lower_wall = 0
        self.left_wall = 0

    def __repr__(self):
        return f"upper {self.upper_wall}, right {self.right_wall}, lower {self.lower_wall}, left{self.left_wall}"


class CellDimention:
    width = 80
    height = 80



class Drawing:

    def __init__(self):
        self.cell_dimentions = CellDimention()

    def get_walls(self, number: int):
        cell = Cell()
        if number & 0B00000001:
            cell.upper_wall = 1
        if number & 0B00000010:
            cell.right_wall = 1
        if number & 0B00000100:
            cell.lower_wall = 1
        if number & 0B00001000:
            cell.left_wall = 1
        return cell

    def draw_maze(self, maze: list, poses_start):
        dimentions = CellDimention()
        x_start_orig, y_start_orig = poses_start
        x_start, y_start = poses_start
        cell_width, cell_height = dimentions.width, dimentions.height
        for i, list_a in enumerate(maze, start=1):
            for j, node in enumerate(list_a, start=1):
                cell = self.get_walls(node)
                pygame.draw.line(screen, (255, 255, 255), (x_start, y_start), (x_start, y_start), 4)

                if cell.upper_wall:
                    pygame.draw.line(screen, (255, 255, 255), (x_start, y_start), (x_start + cell_width, y_start), 3)
                if cell.left_wall:
                    pygame.draw.line(screen, (255, 255, 255), (x_start, y_start), (x_start, y_start + cell_height), 3)

                if j == 15:
                    if cell.right_wall:
                        pygame.draw.line(screen, (255, 255, 255), (x_start + cell_width, y_start), (x_start + cell_width, y_start + cell_height), 3)

                if i == 15:
                    if cell.lower_wall:
                        pygame.draw.line(screen, (255, 255, 255), (x_start, y_start + cell_height), (x_start + cell_width, y_start + cell_height), 3)

                x_start += cell_width

            x_start = x_start_orig
            y_start += cell_width

    def draw_player(self, pos_start):
        x, y = pos_start
        pygame.draw.rect(screen, (255, 255, 255), (x, y, 14, 14))
        # pygame.draw.rect(screen, (255, 255, 255), (x + 590, y + 590, 14, 14))


if __name__ == "__main__":
    cd = CellDimention()
    width_maze, height_maze = (15 * cd.width , 15 * cd.height)
    width_window, height_window = (2600, 2000)

    maze_engine = MazeGenerator()
    maze = maze_engine.maze
    drawing = Drawing()
    run = True

    screen = pygame.display.set_mode((width_window, height_window))
    pygame.display.set_caption("Pac-Man")

    x = (width_window // 2) - (width_maze//2)
    y = (height_window // 2) - (height_maze//2)
    start_pos = (x, y)
    start_pos_player = (x + width_maze // 2, y + height_maze // 2)

    while run:
        pygame.time.delay(100)
        drawing.draw_maze(maze, start_pos)
        drawing.draw_player(start_pos_player)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

        screen.fill((0, 0, 0))
