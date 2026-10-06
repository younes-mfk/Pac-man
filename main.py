from mazegenerator.mazegenerator import MazeGenerator
from UI import Menu
import pygame
from adapter import Adapter
from drawing import Drawing
from ghost_maker import GhostsMaker
from game_play import GamePlay
from pacman_player import PacMan
# from parse_config import GameData


diction_direction = {
        pygame.K_RIGHT: "r",
        pygame.K_LEFT: "l",
        pygame.K_UP: "u",
        pygame.K_DOWN: "d"}


class Main():
    maze_engine = MazeGenerator()  # 14, 10 the min for 42 logo  (14, 10) --> (25, 21)

    def main(self):
        # ############# screen initialization ###########
        screen = pygame.display.set_mode((2600, 2000))
        pygame.display.set_caption("Pac-Man")

        # ############# maze initialization ###########
        maze = self.maze_engine.maze

        # ############# helpers ###########
        adapter = Adapter(maze, (2600, 2000))
        drawing = Drawing(adapter, screen)
        ghoste_creater = GhostsMaker()
        G = GamePlay()
        menu = Menu(screen)

        run = True
        state = "menu"

        while run:

            if state == "menu":
                # data_of_game = GameData()

                pacman = PacMan(adapter.player_position)
                ghosts = ghoste_creater.create_ghosts(adapter.spawn_corners,
                                                      maze,
                                                      adapter.player_position,
                                                      [320, 200, 130, 130],
                                                      adapter.grad_to_window)
                state = menu.run()

            if state == "gameplay":
                state = G.run_the_gam(drawing, maze, adapter, ghosts,
                                      screen, diction_direction,
                                      pacman)

            if state == "exit":
                run = False


if __name__ == "__main__":
    main = Main()
    main.main()
