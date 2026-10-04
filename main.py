from mazegenerator.mazegenerator import MazeGenerator
from ghosts import Ghost
import pygame

diction_direction = {
        pygame.K_RIGHT: "r",
        pygame.K_LEFT: "l",
        pygame.K_UP: "u",
        pygame.K_DOWN: "d"}


class Move:
    pacman = [pygame.image.load("images/pacman_player_right_open.png"),
              pygame.image.load("images/pacman_player_left_open.png"),
              pygame.image.load("images/pacman_player_down_open.png"),
              pygame.image.load("images/pacman_player_up_open.png"),
              pygame.image.load("images/pacman_closed_right_close.png"),
              pygame.image.load("images/pacman_closed_left_close.png"),
              pygame.image.load("images/pacman_closed_down_close.png"),
              pygame.image.load("images/pacman_closed_up_close.png")
              ]

    images = {
        "r": [pacman[0], pacman[4]],
        "l": [pacman[1], pacman[5]],
        "d": [pacman[2], pacman[6]],
        "u": [pacman[3], pacman[7]],
        "": [pacman[3], pacman[7]],
    }

    def __init__(self, current_pos, next_pos, current_frame_pos_x, current_frame_pos_y):
        self.current_pos = current_pos
        self.target = next_pos
        self.current_frame_x = current_frame_pos_x
        self.current_frame_y = current_frame_pos_y
        self.direction = ""
        self.axis = ""
        self.image = pygame.image.load("images/pacman_closed_up_close.png")
        self.image_ghost = pygame.image.load("ghosts_images/ghost.png")


class CellDimention:
    width = 80
    height = 80


class Adapter:
    #  this class to make calculs dynamic and varie with the variation of maze and window dimentions you put
    def __init__(self, maze, window_dimention = (2600, 2000)):
        self.maze = maze
        self.cell_dimontions = CellDimention
        self.window_dimentions = window_dimention
        self.maze_dimentions = ((len(maze[0]) * self.cell_dimontions.width), (len(maze) * self.cell_dimontions.height))
        self.start_drawing_point = ((self.window_dimentions[0] // 2) - (self.maze_dimentions[0]//2),
                                    (self.window_dimentions[1] // 2) - (self.maze_dimentions[1]//2))
        if len(maze[0]) % 2 == 0:
            self.player_position_x = (self.start_drawing_point[0] + (self.maze_dimentions[0] // 2) - self.cell_dimention.width // 2)

        else:
            self.player_position_x = (self.start_drawing_point[0] + self.maze_dimentions[0] // 2)

        if len(maze) % 2 == 0:
            self.player_position_y = (self.start_drawing_point[1] + (self.maze_dimentions[1] // 2) - self.cell_dimention.height // 2)

        else:
            self.player_position_y = (self.start_drawing_point[1] + (self.maze_dimentions[1] // 2))

        self.player_position = (self.player_position_x, self.player_position_y)

        self.gums_positions, self.window_to_grad, self.super_gums_positions = self.get_gums_positions(maze)
        self.grad_to_window = {value: key for key, value in self.window_to_grad.items()}

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


class Cell:
    def __init__(self):
        self.upper_wall = 0
        self.right_wall = 0
        self.lower_wall = 0
        self.left_wall = 0


class Drawing:
    cell_dimentions = CellDimention()

    def __init__(self, adapter: Adapter):
        self.adapter = adapter

    @classmethod
    def get_walls(cls, number: int):
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

    def draw_maze(self, maze: list):
        x_start_orig, y_start_orig = self.adapter.start_drawing_point
        x_start, y_start = self.adapter.start_drawing_point

        cell_width, cell_height = Drawing.cell_dimentions.width, Drawing.cell_dimentions.height

        for y, list_a in enumerate(maze, start=1):
            for x, node in enumerate(list_a, start=1):

                cell = Drawing.get_walls(node)

                if node == 15:
                    pygame.draw.rect(screen, (255, 255, 255), (x_start, y_start, adapter.cell_dimontions.width, adapter.cell_dimontions.height))
                if cell.upper_wall:
                    pygame.draw.line(screen, (0, 0, 255), (x_start, y_start), (x_start + cell_width, y_start), 8)

                if cell.left_wall:
                    pygame.draw.line(screen, (0, 0, 255), (x_start, y_start), (x_start, y_start + cell_height), 8)

                if x == len(list_a):
                    if cell.right_wall:
                        pygame.draw.line(screen, (0, 0, 255), (x_start + cell_width, y_start), (x_start + cell_width, y_start + cell_height), 8)

                if y == len(maze):
                    if cell.lower_wall:
                        pygame.draw.line(screen, (0, 0, 255), (x_start, y_start + cell_height), (x_start + cell_width, y_start + cell_height), 8)

                x_start += cell_width

            x_start = x_start_orig
            y_start += cell_height

    def draw_gums(self, gum_poses):
        for i, j in gum_poses:
            x, y = adapter.window_to_grad[(i, j)]
            node = adapter.maze[y][x]
            if node == 15:
                pass

            elif (x, y) in adapter.super_gums_positions:
                pygame.draw.circle(screen, (255, 255, 45), (i, j), 7)
            else:
                pygame.draw.circle(screen, (255, 255, 255), (i, j), 3)

    def cheeck_colistion(self, current_pos, prev_pos, dr):
        current_position_in_grad_ = adapter.window_to_grad.get(current_pos, None)
        old_position_grad_old = adapter.window_to_grad.get(prev_pos, None)

        if not current_position_in_grad_ or not old_position_grad_old:
            return 0

        node_to = adapter.maze[current_position_in_grad_[1]][current_position_in_grad_[0]]
        node_from = adapter.maze[old_position_grad_old[1]][old_position_grad_old[0]]
        cell_to = Drawing.get_walls(node_to)
        cell_from = Drawing.get_walls(node_from)

        if dr == 'r':
            if cell_from.right_wall or cell_to.left_wall:
                return 0
        if dr == 'l':
            if cell_from.left_wall or cell_to.right_wall:
                return 0

        if dr == 'u':
            if cell_from.upper_wall or cell_to.lower_wall:
                return 0

        if dr == 'd':
            if cell_from.lower_wall or cell_to.upper_wall:
                return 0

        return 1

    def draw_player(self, pos_player, image):

        screen.blit(image, (player_position[0] - 25, player_position[1] - 25))

        if pos_player in adapter.gums_positions:
            adapter.gums_positions.remove(pos_player)
        return pos_player

    def draw_ghost(self, ghost, player_pos, ghostp):

        screen.blit(ghost.image, (ghostp[0] - 20, ghostp[1] - 20))

        if player_pos:
            ghost.player_pos = player_pos

        if adapter.window_to_grad.get(ghostp, None):
            ghost.current_coords = ghost.next_cell(ghost.current_coords, ghost.player_pos)

        return ghostp, adapter.grad_to_window[ghost.current_coords]


if __name__ == "__main__":

    cell_dimention = CellDimention()
    maze_engine = MazeGenerator()
    maze = maze_engine.maze
    adapter = Adapter(maze, (2600, 2000))
    drawing = Drawing(adapter)

    width_window, height_window = adapter.window_dimentions
    width_maze, height_maze = adapter.maze_dimentions
    start_point_drawin_maze = adapter.start_drawing_point
    player_pos_x, player_pos_y = adapter.player_position
    gums_poses = adapter.gums_positions

    screen = pygame.display.set_mode((width_window, height_window))
    pygame.display.set_caption("Pac-Man")
    run = True
    ghost = Ghost((0, 0), pygame.image.load("ghosts_images/ghost.png"), "normal", maze, adapter.player_position)
    clock = pygame.time.Clock()
    speed = 470  # pixels per second

    move = Move(adapter.player_position, adapter.player_position, float(adapter.player_position_x), float(adapter.player_position_y))

    ghost_pos = adapter.grad_to_window[(0, 0)]
    ghost_target = ghost_pos
    ghost_move = Move(ghost_pos, ghost_target, float(ghost_pos[0]), float(ghost_pos[1]))


    times = 1
    open_mouth = 0
    while run:

        if times % 20 == 0:
            if open_mouth:
                open_mouth = 0
            else:
                open_mouth = 1
            times = 1

        r = clock.tick(100)
        dt = r / 1000

        drawing.draw_maze(maze)
        drawing.draw_gums(adapter.gums_positions)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False
                elif event.key in [pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT]:
                    move.direction = diction_direction[event.key]

        if move.current_frame_x == move.target[0] and move.current_frame_y == move.target[1] :

            if move.direction == "r":
                new = (move.current_pos[0] + cell_dimention.width, move.current_pos[1])
                if drawing.cheeck_colistion(new, move.current_pos, 'r'):
                    move.target = (new[0], new[1])
                    move.current_pos = new
                    move.axis = "x"

            if move.direction == "l":
                new = (move.current_pos[0] - cell_dimention.width, move.current_pos[1])
                if drawing.cheeck_colistion(new, move.current_pos, 'l'):
                    move.target = (new[0], new[1])
                    move.current_pos = new
                    move.axis = "x"

            if move.direction == "u":
                new = (move.current_pos[0], move.current_pos[1] - cell_dimention.height)
                if drawing.cheeck_colistion(new, move.current_pos, 'u'):
                    move.target = (new[0], new[1])
                    move.current_pos = new
                    move.axis = "y"

            if move.direction == "d":
                new = (move.current_pos[0], move.current_pos[1] + cell_dimention.height)
                if drawing.cheeck_colistion(new, move.current_pos, 'd'):
                    move.target = (new[0], new[1])
                    move.current_pos = new
                    move.axis = "y"

            move.image = Move.images[move.direction][open_mouth]

        if ghost_move.current_frame_x < ghost_move.target[0]:
            ghost_move.current_frame_x += speed * dt
            if ghost_move.current_frame_x > ghost_move.target[0]:
                ghost_move.current_frame_x = ghost_move.target[0]

        elif ghost_move.current_frame_x > ghost_move.target[0]:
            ghost_move.current_frame_x -= speed * dt
            if ghost_move.current_frame_x < ghost_move.target[0]:
                ghost_move.current_frame_x = ghost_move.target[0]

        if ghost_move.current_frame_y < ghost_move.target[1]:
            ghost_move.current_frame_y += speed * dt
            if ghost_move.current_frame_y > ghost_move.target[1]:
                ghost_move.current_frame_y = ghost_move.target[1]

        elif ghost_move.current_frame_y > ghost_move.target[1]:
            ghost_move.current_frame_y -= speed * dt
            if ghost_move.current_frame_y < ghost_move.target[1]:
                ghost_move.current_frame_y = ghost_move.target[1]

        if move.axis == "x":
            if move.current_frame_x < move.target[0]:
                move.current_frame_x += speed * dt
                if move.current_frame_x > move.target[0]:
                    move.current_frame_x = move.target[0]

            elif move.current_frame_x > move.target[0]:
                move.current_frame_x -= speed * dt
                if move.current_frame_x < move.target[0]:
                    move.current_frame_x = move.target[0]

        elif move.axis == "y":
            if move.current_frame_y < move.target[1]:
                move.current_frame_y += speed * dt
                if move.current_frame_y > move.target[1]:
                    move.current_frame_y = move.target[1]

            elif move.current_frame_y > move.target[1]:
                move.current_frame_y -= speed * dt
                if move.current_frame_y < move.target[1]:
                    move.current_frame_y = move.target[1]

        player_position = (round(move.current_frame_x), round(move.current_frame_y))
        ghost_position = (round(ghost_move.current_frame_x), round(ghost_move.current_frame_y))

        drawing.draw_player(player_position, move.image)
        ghost_move.current_pos, ghost_move.target = drawing.draw_ghost(ghost, adapter.window_to_grad.get(player_position, None), ghost_position)
        if move.current_pos == ghost_move.current_pos or move.current_pos == ghost_move.target:
            move = Move(adapter.player_position, adapter.player_position, float(adapter.player_position_x), float(adapter.player_position_y))

        pygame.display.flip()
        screen.fill((0, 0, 0))

        times += 1
