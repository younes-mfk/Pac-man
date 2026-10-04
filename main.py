from mazegenerator.mazegenerator import MazeGenerator
from ghosts import Ghost
from menu import Menu
import pygame
from moves import Move
from cell import Cell, CellDimention
from adapter import Adapter
import math


diction_direction = {
        pygame.K_RIGHT: "r",
        pygame.K_LEFT: "l",
        pygame.K_UP: "u",
        pygame.K_DOWN: "d"}


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


    def next_frame(self, current_z, target_z, speed, dt):
        returned = current_z

        if current_z < target_z:
            returned += speed * dt
            if returned > target_z:
                returned = target_z

        elif current_z > target_z:
            returned -= speed * dt
            if returned < target_z:
                returned = target_z

        return returned

    def is_colliding(self, pacman, ghost, threshold=40):
        dx = pacman[0] - ghost[0]
        dy = pacman[1] - ghost[1]
        return math.sqrt(dx * dx + dy * dy) < threshold

if __name__ == "__main__":

    cell_dimention = CellDimention()
    maze_engine = MazeGenerator(size=(25, 21))  # 14, 10 the min for 42 logo  (14, 10) --> (25, 21)
    maze = maze_engine.maze
    adapter = Adapter(maze, (2600, 2000))
    # adapter = Adapter(maze, (3600, 2000))
    drawing = Drawing(adapter)

    width_window, height_window = adapter.window_dimentions
    width_maze, height_maze = adapter.maze_dimentions
    start_point_drawin_maze = adapter.start_drawing_point
    player_pos_x, player_pos_y = adapter.player_position
    gums_poses = adapter.gums_positions

    screen = pygame.display.set_mode((width_window, height_window))
    pygame.display.set_caption("Pac-Man")
    run = True
    clock = pygame.time.Clock()
    speed = 470  # pixels per second
    move = Move(adapter.player_position, adapter.player_position, float(adapter.player_position_x), float(adapter.player_position_y))

    ####################################################################################################################
    ghost = Ghost((0, 0), pygame.image.load("ghosts_images/ghost.png"), "normal", maze, adapter.player_position)
    ghost2 = Ghost((14, 14), pygame.image.load("ghosts_images/ghost.png"), "normal", maze, adapter.player_position)
    ghost3 = Ghost((14, 0), pygame.image.load("ghosts_images/ghost.png"), "random", maze, adapter.player_position)
    ghost4 = Ghost((0, 14), pygame.image.load("ghosts_images/ghost.png"), "random", maze, adapter.player_position)

    ghosts = [ghost, ghost2, ghost3, ghost4]

    ghost_pos = adapter.grad_to_window[(0, 0)]
    ghost_target = ghost_pos
    ghost_move = Move(ghost_pos, ghost_target, float(ghost_pos[0]), float(ghost_pos[1]))

    ghost_pos2 = adapter.grad_to_window[(14, 14)]
    ghost_target2 = ghost_pos2
    ghost_move2 = Move(ghost_pos2, ghost_target2, float(ghost_pos2[0]), float(ghost_pos2[1]))

    ghost_pos3 = adapter.grad_to_window[(14, 0)]
    ghost_target3 = ghost_pos3
    ghost_move3 = Move(ghost_pos3, ghost_target3, float(ghost_pos3[0]), float(ghost_pos3[1]))

    ghost_pos4 = adapter.grad_to_window[(0, 14)]
    ghost_target4 = ghost_pos4
    ghost_move4 = Move(ghost_pos4, ghost_target4, float(ghost_pos4[0]), float(ghost_pos4[1]))

    moved_ghosts = [ghost_move, ghost_move2, ghost_move3, ghost_move4]
    ghosts_poses = []

    ####################################################################################################################
    menu = Menu(screen, pygame.image.load("menu_images/menu.png"),
                [pygame.image.load("menu_images/startgame.png"),
                 pygame.image.load("menu_images/instruction.png"),
                 pygame.image.load("menu_images/high_scores.png")])

    menu.test()

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

        if move.current_frame_x == move.target[0] and move.current_frame_y == move.target[1]:

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

        # get frames to draw
        move.current_frame_x = drawing.next_frame(move.current_frame_x, move.target[0], speed, dt)
        move.current_frame_y = drawing.next_frame(move.current_frame_y, move.target[1], speed, dt)
        player_position = (round(move.current_frame_x), round(move.current_frame_y))

        for i, ghost in enumerate(moved_ghosts):
            if i == 0:
                ghost.current_frame_x = drawing.next_frame(ghost.current_frame_x, ghost.target[0], speed - 70, dt)
                ghost.current_frame_y = drawing.next_frame(ghost.current_frame_y, ghost.target[1], speed - 70, dt)
            elif i == 1:
                ghost.current_frame_x = drawing.next_frame(ghost.current_frame_x, ghost.target[0], speed - 80, dt)
                ghost.current_frame_y = drawing.next_frame(ghost.current_frame_y, ghost.target[1], speed - 80, dt)
            else:
                ghost.current_frame_x = drawing.next_frame(ghost.current_frame_x, ghost.target[0], speed - 60, dt)
                ghost.current_frame_y = drawing.next_frame(ghost.current_frame_y, ghost.target[1], speed - 60, dt)

            ghosts_poses.append((round(ghost.current_frame_x), round(ghost.current_frame_y)))

        drawing.draw_player(player_position, move.image)

        for i, ghost_position in enumerate(ghosts_poses):
            moved_ghosts[i].current_pos, moved_ghosts[i].target = drawing.draw_ghost(ghosts[i], adapter.window_to_grad.get(player_position, None), ghost_position)

            # if move.current_pos == moved_ghosts[i].current_pos or move.current_pos == moved_ghosts[i].target:
            if drawing.is_colliding((move.current_frame_x, move.current_frame_y),(moved_ghosts[i].current_frame_x,moved_ghosts[i].current_frame_y)):
                drawing.draw_player(player_position, move.image)

                move = Move(adapter.player_position, adapter.player_position, float(adapter.player_position_x), float(adapter.player_position_y))
                if i:
                    moved_ghosts[i] = Move(ghost_pos, ghost_target, float(ghost_pos[0]), float(ghost_pos[1]))
                    ghosts[i] = Ghost((0, 0), pygame.image.load("ghosts_images/ghost.png"), "normal", maze, adapter.player_position)
                elif i == 1:
                    moved_ghosts[i] = Move(ghost_pos2, ghost_target2, float(ghost_pos2[0]), float(ghost_pos2[1]))
                    ghosts[i] = Ghost((14, 14), pygame.image.load("ghosts_images/ghost.png"), "normal", maze, adapter.player_position)
                elif i == 2:
                    moved_ghosts[i] = Move(ghost_pos3, ghost_target3, float(ghost_pos3[0]), float(ghost_pos3[1]))
                    ghosts[i] = Ghost((0, 14), pygame.image.load("ghosts_images/ghost.png"), "normal", maze, adapter.player_position)
                elif i == 4:
                    moved_ghosts[i] = Move(ghost_pos4, ghost_target4, float(ghost_pos4[0]), float(ghost_pos4[1]))
                    ghosts[i] = Ghost((14, 0), pygame.image.load("ghosts_images/ghost.png"), "normal", maze, adapter.player_position)


            ghosts_poses = []


        pygame.display.flip()
        screen.fill((0, 0, 0))

        times += 1
