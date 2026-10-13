from cell import Cell, CellDimention
from adapter import Adapter
import pygame
import math
from typing import List, Tuple
from pacman_player import PacMan
from ghosts import Ghost


class Drawing:
    """ The class responsible to draw elements of the game """

    cell_dimentions = CellDimention()

    def __init__(self, adapter: Adapter, screen: pygame.Surface) -> None:
        """ Initialize the Drawing class
        Args:
            adapter: the adapter obj
            screen: the sreen obj to draw in it
        """

        self.adapter = adapter
        self.screen = screen

    @classmethod
    def get_walls(cls, number: int) -> Cell:
        """ Transforme the value of node to walls representation
        Args:
            number: the value of node
        Return:
            cell: Cell obj that contains the walls representation
        """

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

    def draw_maze(self, maze: List) -> None:
        """  draw the maze
        Args:
            maze: 2D array representation of the maze
        """

        x_start_orig, y_start_orig = self.adapter.start_drawing_point
        x_start, y_start = self.adapter.start_drawing_point

        (cell_width, cell_height) = (Drawing.cell_dimentions.width,
                                     Drawing.cell_dimentions.height)

        for y, list_a in enumerate(maze, start=1):
            for x, node in enumerate(list_a, start=1):

                cell = Drawing.get_walls(node)

                if node == 15:
                    pygame.draw.rect(self.screen, (255, 255, 255), (x_start,
                                     y_start,
                                     self.adapter.cell_dimontions.width,
                                     self.adapter.cell_dimontions.height))

                if cell.upper_wall:
                    pygame.draw.line(self.screen, (0, 0, 255),
                                     (x_start, y_start),
                                     (x_start + cell_width, y_start), 8)

                if cell.left_wall:
                    pygame.draw.line(self.screen, (0, 0, 255),
                                     (x_start, y_start),
                                     (x_start, y_start + cell_height), 8)

                if x == len(list_a):
                    if cell.right_wall:
                        pygame.draw.line(self.screen, (0, 0, 255),
                                         (x_start + cell_width, y_start),
                                         (x_start + cell_width, y_start +
                                          cell_height), 8)

                if y == len(maze):
                    if cell.lower_wall:
                        pygame.draw.line(self.screen, (0, 0, 255),
                                         (x_start, y_start + cell_height),
                                         (x_start + cell_width, y_start +
                                          cell_height), 8)

                x_start += cell_width

            x_start = x_start_orig
            y_start += cell_height

    def draw_gums(self, gum_poses: List) -> None:
        """ Draw the gums in the maze
        Args:
            gum_poses: the list of gums positions
        """
        for i, j in gum_poses:
            x, y = self.adapter.window_to_grad[(i, j)]
            node = self.adapter.maze[y][x]
            if node == 15:
                pass

            elif (x, y) in self.adapter.super_gums_positions:
                pygame.draw.circle(self.screen, (255, 255, 45), (i, j), 7)
            else:
                pygame.draw.circle(self.screen, (255, 255, 255), (i, j), 3)

    def draw_map_and_gums(self, maze: List, gum_poses: List) -> None:
        """Draw the maze and the gums

        Args:
            maze: The maze to draw.
            gum_poses: The positions of the gums to draw
        """

        self.draw_maze(maze)
        self.draw_gums(gum_poses)

    def cheeck_colistion(self, current_pos: Tuple, prev_pos: Tuple,
                         dr: str) -> int:
        """Check whether movement between two positions is allowed

        Args:
            current_pos: The position the player wants to move to.
            prev_pos: The previous position of the player.
            dr: The movement direction ('r', 'l', 'u', or 'd').

        Returns:
            1 if movement is allowed, or 0 if a wall blocks movement
        """

        current_in_grad_ = self.adapter.window_to_grad.get(current_pos, None)
        old_grad_old = self.adapter.window_to_grad.get(prev_pos, None)

        if not current_in_grad_ or not old_grad_old:
            return 0

        node_to = self.adapter.maze[current_in_grad_[1]][current_in_grad_[0]]
        node_from = self.adapter.maze[old_grad_old[1]][old_grad_old[0]]
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

    def draw_player(self, pacman: PacMan) -> None:
        """Draw pacman and handle gum collection

        Args:
            pacman: The Pac-Man instance to draw and update.
        """

        pos_player = pacman.current_frame
        image = pacman.move.image
        self.screen.blit(image, (pos_player[0] - 25, pos_player[1] - 25))

        if pos_player in self.adapter.gums_positions:
            self.adapter.gums_positions.remove(pos_player)
            if (self.adapter.window_to_grad[pos_player] in
                    self.adapter.super_gums_positions):

                self.adapter.super_gums_positions.remove(
                    self.adapter.window_to_grad[pos_player])

                pacman.data_of_game.ate_supergum()
            else:
                pacman.data_of_game.ate_gum()

    def draw_ghost(self, ghost: Ghost, player_pos: Tuple,
                   ghost_pos: Tuple) -> None:
        """Draw a ghost and update its movement information

        Args:
            ghost: The ghost obj to draw and update
            player_pos: The player's current position
            ghost_pos: The ghost's current drawing position
        """

        self.screen.blit(ghost.image, (ghost_pos[0] - 20, ghost_pos[1] - 20))

        if player_pos:
            ghost.player_pos = player_pos

        if self.adapter.window_to_grad.get(ghost_pos, None):
            ghost.current_coords = ghost.next_cell(ghost.current_coords,
                                                   ghost.player_pos)

        ghost.move.current_pos = ghost_pos
        ghost.move.target = self.adapter.grad_to_window[ghost.current_coords]

    def collusion(self, pacman: Tuple, ghost: Tuple, spaces: int = 40) -> bool:
        """Check if pacman and a ghost are close enough to collide

        Args:
            pacman: pacman position
            ghost: The ghost position
            spaces: The distance threshold for a collision

        Returns:
            true if the distance between the positions is less than
            40 pixel, otherwise False
        """

        dx = pacman[0] - ghost[0]
        dy = pacman[1] - ghost[1]
        return math.sqrt(dx * dx + dy * dy) < spaces

    def update_pacman_move(self, pacman: PacMan, open_mouth: int) -> None:
        """Update pacman's movement and animation

        Args:
            pacman: The Pacman obj
            open_mouth: The animation frame index used to select the image
        """

        if pacman.move.direction == "r":

            new = (pacman.move.current_pos[0] + self.cell_dimentions.width,
                   pacman.move.current_pos[1])

            if self.cheeck_colistion(new, pacman.move.current_pos, 'r'):
                pacman.move.target = (new[0], new[1])
                pacman.move.current_pos = new
                pacman.move.axis = "x"

        if pacman.move.direction == "l":

            new = (pacman.move.current_pos[0] - self.cell_dimentions.width,
                   pacman.move.current_pos[1])

            if self.cheeck_colistion(new, pacman.move.current_pos, 'l'):
                pacman.move.target = (new[0], new[1])
                pacman.move.current_pos = new
                pacman.move.axis = "x"

        if pacman.move.direction == "u":

            new = (pacman.move.current_pos[0],
                   pacman.move.current_pos[1] - self.cell_dimentions.height)

            if self.cheeck_colistion(new, pacman.move.current_pos, 'u'):
                pacman.move.target = (new[0], new[1])
                pacman.move.current_pos = new
                pacman.move.axis = "y"

        if pacman.move.direction == "d":

            new = (pacman.move.current_pos[0],
                   pacman.move.current_pos[1] + self.cell_dimentions.height)

            if self.cheeck_colistion(new, pacman.move.current_pos, 'd'):
                pacman.move.target = (new[0], new[1])
                pacman.move.current_pos = new
                pacman.move.axis = "y"

        if pacman.mortal is False:
            img = pacman.move.respawn_images[pacman.move.direction][open_mouth]
            pacman.move.image = img

        else:
            img = pacman.move.images[pacman.move.direction][open_mouth]
            pacman.move.image = img
