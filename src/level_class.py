from mazegenerator.mazegenerator import MazeGenerator
from adapter import Adapter
from drawing import Drawing
from typing import List
from ghost_maker import GhostsMaker
import pygame


class Level:
    """ the class to restart everything related to the maze changing through
        the levels
    """

    def __init__(self, maze: List, adapter: Adapter, drawing: Drawing,
                 ghosts: List) -> None:
        """ Initialize the obj attributes
            Args:
                maze: 2D array representqtion of the maze
                adapter: the adapter obj
                drawing: the obj responsable to draw elements
                ghosts: list of ghosts alive
            """

        self.maze = maze
        self.adapter = adapter
        self.drawing = drawing
        self.ghosts = ghosts


class LevelFactory:
    """ the class that reproduce a random maze and faster ghosts"""

    speeds = [100, 100, 140, 140]
    added_speed = 35

    def __init__(self, screen: pygame.Surface, ghosts_maker: GhostsMaker,
                 base_seed: int = 0) -> None:
        """ Initialize the obj attributes
            Args:
                screen: the screen obj to draw in it
                ghosts_maker: an obj to ghosts factory class
                based_seed: int to controle the maze randomness
        """

        self.screen = screen
        self.ghosts_maker = ghosts_maker
        self.base_seed = base_seed

    def up_ghost_speeds(self, number: int) -> List:
        """ a simple calculs that depende on the level to
            augment the ghosts speed
            Args:
                number: the level ze on now
        """

        return [speed + self.added_speed * (number - 1) for
                speed in self.speeds]

    def create(self, number: int, seed: int) -> Level:
        """ create the new elements when new maze maked
            Args:
                number: the level ze on now
                seed: int to controle the maze randomness
        """

        maze = MazeGenerator(size=(20, 20), seed=seed).maze
        adapter = Adapter(maze)
        drawing = Drawing(adapter, self.screen)
        ghosts = self.ghosts_maker.create_ghosts(adapter.spawn_corners,
                                                 maze,
                                                 adapter.player_position,
                                                 self.up_ghost_speeds(number),
                                                 adapter.grad_to_window)

        return Level(maze, adapter, drawing, ghosts)
