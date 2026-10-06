from mazegenerator.mazegenerator import MazeGenerator
# from menu import Menu
# from ghosts import Ghost
from ghosts import Ghost
from UI import Menu
import pygame
from moves import Move
from cell import CellDimention
from adapter import Adapter
from drawing import Drawing
from ghost_maker import GhostsMaker
from game_play import GamePlay
from pacman_player import PacMan

diction_direction = {
        pygame.K_RIGHT: "r",
        pygame.K_LEFT: "l",
        pygame.K_UP: "u",
        pygame.K_DOWN: "d"}


if __name__ == "__main__":

    maze_engine = MazeGenerator(size=(15, 15))  # 14, 10 the min for 42 logo  (14, 10) --> (25, 21)
    maze = maze_engine.maze
    screen = pygame.display.set_mode((2600, 2000))
    adapter = Adapter(maze, (2600, 2000))
    pacman = PacMan(adapter.player_position)

    drawing = Drawing(adapter, screen)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Pac-Man")
    G = GamePlay()

    ghoste_creater = GhostsMaker()
    ghosts = ghoste_creater.create_ghosts_obj(adapter.spawn_corners, maze,
                                              adapter.player_position,
                                              [320, 200, 130, 130])

    moved_ghosts = ghoste_creater.create_ghosts_moves(adapter.grad_to_window,
                                                      adapter.spawn_corners)

    run = True

    menu = Menu(screen, pygame.image.load("menu_images/menu.png"),
                [pygame.image.load("menu_images/startgame.png"),
                 pygame.image.load("menu_images/high_scores.png"),
                 pygame.image.load("menu_images/instruction.png"),
                 pygame.image.load("menu_images/exit.png")],
                [pygame.image.load("menu_images/selected_startgame.png"),
                 pygame.image.load("menu_images/selected_high_scores.png"),
                 pygame.image.load("menu_images/selected_instructions.png"),
                 pygame.image.load("menu_images/selected_exit.png")])
    state = "menu"
    while run:

        if state == "menu":
            state = menu.run()

        if state == "gameplay":
            state = run = run = G.run_the_gam(drawing, maze, adapter, ghosts,
                                              moved_ghosts,
                                              screen, diction_direction,
                                              pacman)
