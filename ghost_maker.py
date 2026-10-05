from ghosts import Ghost
import pygame
from moves import Move


class GhostsMaker:
    image = pygame.image.load("ghosts_images/ghost.png")

    def create_ghosts_obj(self, spawn_corners: int, maze, player_position,
                          speed):

        ghosts = []

        for i, pos in enumerate(spawn_corners):
            if i % 2 == 0:
                ghosts.append(Ghost(pos,  GhostsMaker.image, "normal", maze,
                                    player_position, speed[i]))
            else:
                ghosts.append(Ghost(pos,  GhostsMaker.image, "random", maze,
                                    player_position, speed[i]))

        return ghosts

    def create_ghosts_moves(self, grad_to_window, spawn_corners):

        moved_ghosts = [Move(grad_to_window[pos], grad_to_window[pos],
                             float(grad_to_window[pos][0]),
                             float(grad_to_window[pos][1]),
                             grad_to_window[pos]) for pos in spawn_corners]
        return moved_ghosts
