from mazegenerator.mazegenerator import MazeGenerator
from UI import Menu, GameOver, Victory
from db import DataBase
import pygame
from adapter import Adapter
from drawing import Drawing
from ghost_maker import GhostsMaker
from game_play import GamePlay
from pacman_player import PacMan
from cell import Window
from level_class import LevelFactory
from typing import Tuple, List


class Main():
    window = Window()

    def set_up(self, screen: pygame.Surface,
               speeds: List = [100, 100, 140, 140]) -> Tuple:
        maze_engine = MazeGenerator(size=(5, 5), seed=42)
        maze = maze_engine.maze

        ghoste_creater = GhostsMaker()
        adapter = Adapter(maze, (self.window.width,
                                 self.window.height))

        drawing = Drawing(adapter, screen)
        pacman = PacMan(adapter.player_position)
        ghosts = ghoste_creater.create_ghosts(adapter.spawn_corners,
                                              maze,
                                              adapter.player_position,
                                              speeds,
                                              adapter.grad_to_window)

        return (adapter, pacman, ghosts, drawing, maze)

    def main(self) -> None:
        screen = pygame.display.set_mode((self.window.width,
                                          self.window.height))
        pygame.display.set_caption("Pac-Man")

        levels = LevelFactory(screen, GhostsMaker(), base_seed=42)
        G = GamePlay(levels)

        # ############## Windows ####################
        database = DataBase()
        menu = Menu(screen, database)
        gameover = GameOver(screen, database)
        victory = Victory(screen, database)

        run = True
        state: str | None = "menu"

        while run:

            if state == "menu":
                adapter, pacman, ghosts, drawing, maze = self.set_up(screen)
                state = menu.run()

            if state == "gameplay":
                state = G.run_the_gam(drawing, maze, adapter, ghosts,
                                      screen,
                                      pacman)

            if state == "game over":
                state = gameover.run(pacman.data_of_game)

            if state == "victory":
                state = victory.run(pacman.data_of_game)

            if state == "exit":
                run = False


if __name__ == "__main__":
    main = Main()
    main.main()
