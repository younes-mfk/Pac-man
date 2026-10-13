from ghosts import Ghost
import pygame
from moves import Move
from paths import PathResolver
from typing import List, Tuple, Dict


class GhostsMaker:
    """Create and restart ghosts for the game"""

    image = pygame.image.load(
        PathResolver.resource_path("ghosts_images/ghost.png"))

    def create_ghosts(self, spawn_corners: List, maze: List,
                      player_position: Tuple,
                      speed: List, grad_to_window: Dict) -> List:
        """Create and initialize the ghosts

        Args:
            spawn_corners: The corner where ghosts spawn
            maze: The maze used by the ghosts
            player_position: The player's current position
            speed: The movement speeds assigned to the ghosts
            grad_to_window: Mapping from grid positions to window positions

        Returns:
            A list of initialized Ghost objs
        """

        ghosts: List = []

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
    def restart_ghost(cls, ghost: Ghost, grad_to_window: Dict,
                      pos_player: Tuple) -> Ghost:
        """Create a replacement ghost at its original spawn position

        Preserves the ghost's maze and speed, updates its player position
        and initializes its movement at the corresponding window position

        Args:
            ghost: The ghost instance to restart
            grad_to_window: Mapping from grid positions to window positions
            pos_player: The player's current position

        Returns:
            A newly initialized Ghost obj
        """

        ghost = Ghost(ghost.spawn_point,
                      GhostsMaker.image, "normal", ghost.maze,
                      pos_player, ghost.speed)

        ghost.move = Move(grad_to_window[ghost.spawn_point],
                          grad_to_window[ghost.spawn_point],
                          float(grad_to_window[ghost.spawn_point][0]),
                          float(grad_to_window[ghost.spawn_point][1]),
                          grad_to_window[ghost.spawn_point])

        return ghost
