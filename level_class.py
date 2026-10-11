from mazegenerator.mazegenerator import MazeGenerator
from adapter import Adapter
from drawing import Drawing
from typing import List, Tuple
from ghost_maker import GhostsMaker
import pygame

class Level:
    def __init__(self, maze: List, adapter: Adapter, drawing: Drawing,
                 ghosts: List) -> None:
        self.maze = maze
        self.adapter = adapter
        self.drawing = drawing
        self.ghosts = ghosts


class LevelFactory:

    speeds = [100, 100, 140, 140]
    added_speed = 35

    def __init__(self, screen: pygame.Surface, ghosts_maker: GhostsMaker,
                 base_seed: int = 0) -> None:
        self.screen = screen
        self.ghosts_maker = ghosts_maker
        self.base_seed = base_seed

    def up_ghost_speeds(self, number: int) -> List:
        return [speed + self.added_speed * (number - 1) for
                speed in self.speeds]

    def create(self, number: int, seed: int) -> Level:
        maze = MazeGenerator(size=(20, 20), seed=seed).maze
        adapter = Adapter(maze)
        drawing = Drawing(adapter, self.screen)
        ghosts = self.ghosts_maker.create_ghosts(adapter.spawn_corners,
                                                 maze,
                                                 adapter.player_position,
                                                 self.up_ghost_speeds(number),
                                                 adapter.grad_to_window)

        return Level(maze, adapter, drawing, ghosts)
