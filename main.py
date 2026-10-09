from mazegenerator.mazegenerator import MazeGenerator
from UI import Menu, GameOver, Victory
from db import DataBase
import pygame
from adapter import Adapter
from drawing import Drawing
from ghost_maker import GhostsMaker
from game_play import GamePlay
from pacman_player import PacMan
# from parse_config import GameData
from cell import Window

diction_direction = {
        pygame.K_RIGHT: "r",
        pygame.K_LEFT: "l",
        pygame.K_UP: "u",
        pygame.K_DOWN: "d"}


class Main():
    # 14, 10 the min for 42 logo  (14, 10) --> (25, 21)
    maze_engine = MazeGenerator(size=(5, 5))
    window = Window()

    def main(self):
        # ############# screen initialization ######################
        screen = pygame.display.set_mode((self.window.width,
                                          self.window.height))
        pygame.display.set_caption("Pac-Man")

        # ############# maze initialization ########################
        maze = self.maze_engine.maze

        # ############# helpers ####################################
        adapter = Adapter(maze, (self.window.width,
                                 self.window.height))
        drawing = Drawing(adapter, screen)
        ghoste_creater = GhostsMaker()
        G = GamePlay()
        database = DataBase()
        menu = Menu(screen, database)
        gameover = GameOver(screen, database)
        victory = Victory(screen, database)

        run = True
        state = "menu"

        while run:

            if state == "menu":
                pacman = PacMan(adapter.player_position)
                ghosts = ghoste_creater.create_ghosts(adapter.spawn_corners,
                                                      maze,
                                                      adapter.player_position,
                                                      [100, 100, 140, 140],
                                                      adapter.grad_to_window)
                state = menu.run()

            if state == "gameplay":
                state = G.run_the_gam(drawing, maze, adapter, ghosts,
                                      screen, diction_direction,
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
