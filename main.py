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
    cell_dimentions = CellDimention()

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
        x_start_orig, y_start_orig = poses_start
        x_start, y_start = poses_start

        cell_width, cell_height = Drawing.cell_dimentions.width, Drawing.cell_dimentions.height

        for i, list_a in enumerate(maze, start=1):
            for j, node in enumerate(list_a, start=1):

                cell = self.get_walls(node)

                # pygame.draw.line(screen, (0, 0, 255), (x_start - 3, y_start - 3), (x_start - 3, y_start - 3), 5)
                # pygame.draw.line(screen, (0, 0, 255), (x_start + 3, y_start + 3), (x_start + 3, y_start + 3), 5)

                pygame.draw.line(screen, (0, 0, 255), (x_start, y_start), (x_start, y_start), 5)

                if cell.upper_wall:
                    pygame.draw.line(screen, (0, 0, 255), (x_start, y_start), (x_start + cell_width, y_start), 6)

                if cell.left_wall:
                    pygame.draw.line(screen, (0, 0, 255), (x_start, y_start), (x_start, y_start + cell_height), 6)

                if j == 15:
                    if cell.right_wall:
                        pygame.draw.line(screen, (0, 0, 255), (x_start + cell_width, y_start), (x_start + cell_width, y_start + cell_height), 6)

                if i == 15:
                    if cell.lower_wall:
                        pygame.draw.line(screen, (0, 0, 255), (x_start, y_start + cell_height), (x_start + cell_width, y_start + cell_height), 6)

                x_start += cell_width

            x_start = x_start_orig
            y_start += cell_width

    def draw_gums(self, maze, dimention):
        x_start_orig, y_start_orig = dimention
        x_start, y_start = dimention
        for i in range(1, 16):
            for j in range(1, 16):
                node = maze[i - 1][j - 1]
                if node == 15:
                    pass
                
                elif (i == 1 or i == 15) and (j == 1 or j == 15):
                    pygame.draw.circle(screen, (255, 255, 45), (x_start + 40, y_start + 40), 7)

                else:
                    pygame.draw.circle(screen, (255, 255, 255), (x_start + 40, y_start + 40), 3)

                x_start += Drawing.cell_dimentions.width

            x_start = x_start_orig
            y_start += Drawing.cell_dimentions.width

    def draw_player(self, pos_start, prev_pos):
        x, y = pos_start
        pygame.draw.circle(screen, (255, 255, 0), (x, y), 5)

        # if self.no_coolision(pos_start):
        #     pygame.draw.circle(screen, (255, 255, 255), (x, y), 5)
        #     return (x, y)
        # pygame.draw.circle(screen, (255, 255, 255), prev_pos, 5)
        # return prev_pos


if __name__ == "__main__":

    cd = CellDimention()
    maze_engine = MazeGenerator()
    drawing = Drawing()

    ##########################################################################
    # THIS PARAMETRE CURRENTLY HERE WE GONNA PASS THEM THROUGHT THE CONFIGE FILE
    # 15 BECAUSE ARE THE DEFAULT GIVEN VALUES TO THE MAZE GENERATOR (LOOK AT PACKAGE)
    width_maze, height_maze = (15 * cd.width, 15 * cd.height)
    width_window, height_window = (2600, 2000)
    ##########################################################################
    maze = maze_engine.maze
    run = True

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width_window, height_window))
    pygame.display.set_caption("Pac-Man")

    x_center = (width_window // 2) - (width_maze//2)
    y_center = (height_window // 2) - (height_maze//2)

    start_point_drawin_maze = (x_center, y_center)
    start_point_of_player = (x_center + width_maze // 2, y_center + height_maze // 2)

    moved_pos_x, moved_pos_y = start_point_of_player

    while run:
        pygame.time.delay(100)

        # r = clock.tick(60)
        # dt = r / 1000

        drawing.draw_maze(maze, start_point_drawin_maze)
        drawing.draw_gums(maze, start_point_drawin_maze)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    moved_pos_x += cd.width
                if event.key == pygame.K_LEFT:
                    moved_pos_x -= cd.width
                if event.key == pygame.K_UP:
                    moved_pos_y -= cd.height
                if event.key == pygame.K_DOWN:
                    moved_pos_y += cd.height

        previos = (moved_pos_x, moved_pos_y)
        events = pygame.key.get_pressed()


        previos = drawing.draw_player((moved_pos_x, moved_pos_y), previos)

        pygame.display.update()
        screen.fill((0, 0, 0))
