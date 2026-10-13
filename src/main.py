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
from typing import Tuple, List, Any, Dict
import json
import sys


class Main():

    """the main class contains the root function of the program """

    window = Window()
    main_keys = ["hearts", "points_per_pacgum",
                 "points_per_superpacgum",
                 "points_per_ghost", "level_time", "cheat_mode"]

    def parser(self, file: str) -> Any:
        """ Parse the provided file
        Args:
            file: the nam eof config file
        return:
            None if the parsing faile, dict config if passed
        """

        clean_json = ""

        try:
            with open(file) as config_file:
                for line in config_file:
                    clean_json += line.split("#")[0]
        except (PermissionError):
            print("permission to read not allowed")
            return False
        except (FileNotFoundError):
            print("File Not Found")
            return False

        try:
            config = json.loads(clean_json)
        except (json.JSONDecodeError):
            print("invalide json config file")
            config = {}

        for key in Main.main_keys:
            if key not in config.keys():
                print(f"the key {key} is missing")
                continue

            if key == "cheat_mode" and config[key] not in (False, True):
                config[key] = False

            if key in ("points_per_pacgum", "points_per_superpacgum",
                       "points_per_ghost", "level_time"):
                if not isinstance(config[key], int) or config[key] <= 0:
                    print(f"{key} value can't be non "
                          "positive number clamp to default 90")

                    if key == "level_time":
                        config[key] = 90
                    else:
                        config[key] = 10

            if key in ("hearts"):
                if not isinstance(config[key], int) or config[key] <= 0:
                    print(f"{key} value can't be non "
                          "positive number clamp to default 3")
                    config[key] = 3

        return config

    def set_up(self, screen: pygame.Surface, parsed_config: Dict,
               speeds: List = [100, 100, 140, 140]) -> Tuple:

        """ set up the elements of the game
        Args:
            screen: the screen obj
            parsed_config: the parsed dict from config file
            speeds: list of speeds of ghosts
        Return:
            adapter: the adapter obj provide the dimentions to draw
            pacman: pacman ob
            ghosts: list of ghosts objs
            drawing: obj for draw game elements
            maze: the 2D array obj
        """
        maze_engine = MazeGenerator(size=(20, 20), seed=42)
        maze = maze_engine.maze

        ghoste_creater = GhostsMaker()
        adapter = Adapter(maze, (self.window.width,
                                 self.window.height))

        drawing = Drawing(adapter, screen)
        pacman = PacMan(adapter.player_position, parsed_config)
        ghosts = ghoste_creater.create_ghosts(adapter.spawn_corners,
                                              maze,
                                              adapter.player_position,
                                              speeds,
                                              adapter.grad_to_window)

        return (adapter, pacman, ghosts, drawing, maze)

    def main(self) -> None:
        """ The main function where evrything start"""

        if len(sys.argv) != 2:
            print("you program should take the config file only as arguments")
            return

        file = sys.argv[1]
        if not file.endswith(".json"):
            print("config file should follow the json format")
            return

        parsed_config = self.parser(file)
        if parsed_config is False:
            return

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
                adapter, pacman, ghosts, drawing, maze = self.set_up(
                    screen, parsed_config)
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
    try:
        main = Main()
        main.main()
    except Exception as err:
        print(f"erro: {err}")
