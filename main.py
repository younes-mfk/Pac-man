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

    def __repr__(self):
        return f"upper {self.upper_wall}, right {self.right_wall}, lower {self.lower_wall}, left{self.left_wall}"


def get_walls(number: int):
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



def draw_maze(maze: list, poses_start):
    x_start_orig, y_start_orig = poses_start
    x_start, y_start = poses_start

    for i, list_a in enumerate(maze, start=1):
        for j, node in enumerate(list_a, start=1):
            cell = get_walls(node)
            # if i == 15 and j == 15:
            pygame.draw.line(screen, (255, 0, 0), (x_start, y_start), (x_start, y_start), 4)

            if cell.upper_wall:
                pygame.draw.line(screen, (255, 0, 0), (x_start, y_start), (x_start + cell_width, y_start), 3)
            if cell.left_wall:
                pygame.draw.line(screen, (255, 0, 0), (x_start, y_start), (x_start, y_start + cell_height), 3)

            if j == 15:
                if cell.right_wall:
                    pygame.draw.line(screen, (255, 0, 0), (x_start + cell_width, y_start), (x_start + cell_width, y_start + cell_height), 3)

            if i == 15:
                if cell.lower_wall:
                    pygame.draw.line(screen, (255, 0, 0), (x_start, y_start + cell_height), (x_start + cell_width, y_start + cell_height), 3)

            x_start += cell_width

        x_start = x_start_orig
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


screen = pygame.display.set_mode((2600, 2000))
pygame.display.set_caption("Pac-Man")

x = (2600 // 2)
y = (2000 // 2)

start_pos = (1000, 1000)

while run:

    pygame.time.delay(100)

    draw_maze(maze, start_pos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

    screen.fill((0, 0, 0))


# if __name__ == "__main__":
#     l = [i for i in range(1, 16)]
#     for i in l:
#         print(i, end=" ")
#         o = get_walls(i)
#         print(o.__repr__())
