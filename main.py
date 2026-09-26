from mazegenerator.mazegenerator import MazeGenerator
import pygame


cell_height = 20
cell_width = 20

class Cell:
    def __init__(self):
        self.upper_wall = 0
        self.right_wall = 0
        self.lower_wall = 0
        self.left_wall = 0


def get_walls(number: int):
    cell = Cell()
    if number & 1:
        cell.upper_wall = 1
    if number & 2:
        cell.right_wall = 1
    if number & 3:
        cell.lower_wall = 1
    if number & 4:
        cell.left_wall = 1
    return cell


def draw_maze(maze: list, poses_start):
    x_start, y_start = poses_start
    for i, list_a in enumerate(maze, start=1):
        for j, node in enumerate(list_a, start=1):
            cell = get_walls(node)
            # if i == 15 and j == 15:
            # pygame.draw.line(screen, (255, 0, 0), (x_start, y_start), (x_start, y_start), 4)

            if cell.upper_wall:
                pygame.draw.line(screen, (255, 0, 0), (x_start, y_start), (x_start + cell_width, y_start), 3)
            if cell.left_wall:
                pygame.draw.line(screen, (255, 0, 0), (x_start, y_start), (x_start, y_start + cell_height), 3)

            if i == 15:
                if cell.right_wall:
                    pygame.draw.line(screen, (255, 0, 0), (x_start + cell_width, y_start), (x_start + cell_width, y_start + cell_height), 3)

            if j == 15:
                if cell.lower_wall:
                    pygame.draw.line(screen, (255, 0, 0), (x_start, y_start + cell_height), (x_start + cell_width, y_start + cell_height), 3)

            x_start += cell_width

        x_start = 100
        y_start += cell_width

            # if i == 15 and j == 15:
            #     pass
            # elif i == 15:
            #     pass
            # elif j == 15:
            #     pass


maze_engine = MazeGenerator()
maze = maze_engine.maze
run = True

start_pos = (100, 100)

screen = pygame.display.set_mode((1200, 1200))
pygame.display.set_caption("Pac-Man")
print(maze)
while run:
    pygame.time.delay(100)
    draw_maze(maze, start_pos)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

    screen.fill((0, 0, 0))
