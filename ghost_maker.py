from ghosts import Ghost
import pygame
from moves import Move
from paths import PathResolver


class GhostsMaker:
    image = pygame.image.load(PathResolver.resource_path("ghosts_images/ghost.png"))

    def create_ghosts(self, spawn_corners: int, maze, player_position,
                      speed, grad_to_window):

        ghosts = []

        for i, pos in enumerate(spawn_corners):
            if i % 2 == 0:
                ghosts.append(Ghost(pos, GhostsMaker.image, "normal", maze,
                                    player_position, speed[i]))
            else:
                ghosts.append(Ghost(pos, GhostsMaker.image, "random", maze,
                                    player_position, speed[i]))

        for i, ghost in enumerate(ghosts):
            ghost.move = Move(grad_to_window[spawn_corners[i]],
                              grad_to_window[spawn_corners[i]],
                              float(grad_to_window[spawn_corners[i]][0]),
                              float(grad_to_window[spawn_corners[i]][1]),
                              grad_to_window[spawn_corners[i]])

        return ghosts

    @classmethod
    def restart_ghost(cls, ghost, grad_to_window, pos_player):

        ghost = Ghost(ghost.spawn_point,
                      GhostsMaker.image, "normal", ghost.maze,
                      pos_player, ghost.speed)

        ghost.move = Move(grad_to_window[ghost.spawn_point],
                          grad_to_window[ghost.spawn_point],
                          float(grad_to_window[ghost.spawn_point][0]),
                          float(grad_to_window[ghost.spawn_point][1]),
                          grad_to_window[ghost.spawn_point])

        return ghost
