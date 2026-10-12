import pygame
from UI import Pausemenu, InGame
from ghost_maker import GhostsMaker
from paths import PathResolver
from level_class import LevelFactory
from typing import List, Tuple, Any
from pacman_player import PacMan
from adapter import Adapter
from ghosts import Ghost
from drawing import Drawing


diction_direction = {
        pygame.K_RIGHT: "r",
        pygame.K_LEFT: "l",
        pygame.K_UP: "u",
        pygame.K_DOWN: "d"}


class GamePlay:

    """manage gameplay logic and game modes"""

    def __init__(self, level_factory: LevelFactory) -> None:

        """Initialize the gameplay manager

        Args:
            level_factory: obj resposible to creating game levels
        """

        self.level_factory = level_factory

    def start_super_mode(self, pacman: PacMan, ghosts: List) -> None:

        """Activate Super Mode for Pac-Man and make ghosts edible

        Args:
            pacman: The Pac-Man instance
            ghosts: List of ghosts objs
        """

        pacman.super = True
        for ghost in ghosts:
            ghost.edible = True
            ghost.image = pygame.image.load(
                PathResolver.resource_path("ghosts_images/ghost_yellow.png"))

    def check_mode_super_time(self, passed_time_super: float, pacman: PacMan,
                              ghosts: List) -> None:
        """Deactivate Super Mode after five seconds

        Args:
            passed_time_super: Time passed since Super Mode started
                                in milliseconds
            pacman: The PacMan obj
            ghosts: list of ghosts
        """
        if passed_time_super / 1000 >= 5:
            pacman.super = False

            for ghost in ghosts:
                ghost.image = pygame.image.load(
                    PathResolver.resource_path("ghosts_images/ghost.png"))
                ghost.edible = False

    def check_pacman_is_alive(self, passed_time_game: float,
                              pacman: PacMan) -> str | None:
        """Check whether PacMan has lost all his lives

        Args:
            passed_time_game: Time since the game started
            pacman: The PacMan instance

        Returns:
            str: "game over" if Pac-Man has no remaining lives else None
        """
        if pacman.data_of_game.hearts == 0:
            return "game over"

        if passed_time_game / 1000 > pacman.data_of_game.level_time:
            return "game over"

        return None

    def respawning_died_ghosts_after_3s(self, waiting_ghosts: List,
                                        ghosts: List,
                                        force: bool = False) -> None:
        """Respawn dead ghosts after three seconds or immediately if forced

        Args:
            waiting_ghosts: List of ghosts waiting to respawn
            ghosts: List of active ghosts
            force: If True, respawn all waiting ghosts immediately
        """
        if force:
            for ghost in (waiting_ghosts[:]):
                ghosts.append(ghost)
                waiting_ghosts.remove(ghost)
        else:
            for ghost in (waiting_ghosts[:]):
                if (
                 (pygame.time.get_ticks() - ghost.respawning_time) //
                 1000 >= 3):
                    ghosts.append(ghost)
                    waiting_ghosts.remove(ghost)

    def level_up(self, pacman: PacMan, waiting_ghosts: List) -> Tuple:
        """Advance to the next level and reset waiting ghosts

        Args:
            pacman: The Pacman instance containing game progress
            waiting_ghosts: List of ghosts waiting to respawn

        Returns:
            tuple: The new level's maze, adapter, drawing object, and ghosts
        """

        pacman.data_of_game.level += 1
        level = self.level_factory.create(pacman.data_of_game.level, 0)
        pacman.new_level(level.adapter.player_position)
        waiting_ghosts.clear()
        return (level.maze, level.adapter, level.drawing, level.ghosts)

    def level_completed(self, adapter: Adapter) -> bool:
        """Check whether the current level has been completed

        Args:
            adapter: Adapter containing the remaining gum positions

        Returns:
            bool: True if no gums remain, otherwise False
        """

        return not len(adapter.gums_positions)

    def check_game_stat(self, pacman: PacMan, adapter: Adapter,
                        time_passed: float) -> None | str:
        """
        Checks whether Pac-Man is dead or the current level is completed

        Args:
            pacman: The Pacman obj
            adapter: Adapter obj
            time_passed: Elapsed game time

        Returns:
            str or None: "game over" if Pac-Man is dead, "level up"
                if the level is completed, or None otherwise.
        """
        state = self.check_pacman_is_alive(time_passed, pacman)
        if state:
            return state

        if self.level_completed(adapter):
            return "level up"

        return None

    def ghost_is_die(self, pacman: PacMan, ghost: Ghost,
                     adapter: Adapter) -> Ghost:
        """Reset a defeated ghost and register its defeat

        Args:
            pacman: The Pacman obj
            ghost: The ghost that was eated
            adapter: Adapter obj

        Returns:
            Ghost: The restarted ghost with its respawn timestamp
        """
        ghost = GhostsMaker.restart_ghost(ghost, adapter.grad_to_window,
                                          pacman.current_frame)
        ghost.respawning_time = pygame.time.get_ticks()

        pacman.data_of_game.ate_ghost()
        return ghost

    def pacman_is_die(self, pacman: PacMan) -> None:
        """Handle Pac-Man's death
        Decreases the remaining lives, resets movement, and temporarily
        makes Pac-Man immortal.

        Args:
            pacman: The PacMan obj
        """
        pacman.data_of_game.hearts -= 1
        pacman.restart_move(pacman)
        pacman.mortal = False
        pacman.time_after_respawning = pygame.time.get_ticks()

    def died_or_win(self, adapter: Adapter, pacman: PacMan,
                    time_down_of_level: float) -> None | str:
        """Check whether the game is over or the level is completed

        Args:
            adapter: Adapter
            pacman: The PacMan obj
            time_down_of_level: time passed for the level

        Returns:
            str or None: The current game state, or None if the game
                should continue
        """
        return self.check_game_stat(pacman, adapter, time_down_of_level)

    def remove_waiting_ghosts_from_ghosts_list(self, waiting_ghosts: List,
                                               ghosts: List) -> None:
        """Remove waiting ghosts from the active ghosts list

        Args:
            waiting_ghosts: List of ghosts waiting to respawn
            ghosts: List of active ghosts
        """
        for ghost in waiting_ghosts:
            if ghost in ghosts:
                ghosts.remove(ghost)

    def remove_imortale_mode_after_2s(self, pacman: PacMan) -> None:
        """Restore Pac-Man's mortal mode after two seconds

        Args:
            pacman: The PacMan
        """
        if pacman.time_after_respawning:
            passed_time = (pygame.time.get_ticks() -
                           pacman.time_after_respawning)
            if passed_time / 1000 >= 2:
                pacman.mortal = True

    def you_win(self, pacman: PacMan) -> bool | None:
        """Check whether Pac-Man has completed the final level.

        Args:
            pacman: The PacMan obj

        Returns:
            bool or None: True if the final level is reached,
                otherwise none
        """
        if pacman.data_of_game.level == 10:
            print("YOU WIN")
            return True
        else:
            return None

    def run_the_gam(self, drawing: Drawing, maze: List, adapter: Adapter,
                    ghosts: List,
                    screen: pygame.Surface, pacman: PacMan) -> Any:
        """Run the main game loop and manage gameplay interactions

        Args:
            drawing: Object responsible for drawing the game elements
            maze: The current level's maze
            adapter: Adapter providing coordinate conversions
            ghosts: list of active ghosts
            screen: pygame surface used to display the game
            pacman: The Pacman instance
        """

        pause_menu = Pausemenu(screen)
        in_game = InGame(screen, adapter)
        run = True
        clock = pygame.time.Clock()
        level_timer = pygame.time.get_ticks()
        waiting_ghosts: List = []

        while run:
            self.remove_waiting_ghosts_from_ghosts_list(waiting_ghosts, ghosts)
            self.respawning_died_ghosts_after_3s(waiting_ghosts, ghosts)
            if self.you_win(pacman):
                return "victory"

            # ################## you in competetive mode ###############
            time_in_level = pygame.time.get_ticks() - level_timer

            state = self.died_or_win(adapter, pacman, time_in_level)

            if state == "game over":
                return state

            if state == "level up":
                maze, adapter, drawing, ghosts = self.level_up(pacman,
                                                               waiting_ghosts)

                in_game = InGame(screen, adapter)
                level_timer = pygame.time.get_ticks()
                continue

            open_mouth = (pygame.time.get_ticks() // 200) % 2
            r = clock.tick(100)
            dt = r / 1000

            # ########################## draw the basics #####################
            drawing.draw_map_and_gums(maze, adapter.gums_positions)

            # ########################## take orders #########################
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    return "exit"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        pacman.data_of_game.cheat_mode = not (
                            pacman.data_of_game.cheat_mode)
                        continue

                    if (event.key == pygame.K_x and
                       pacman.data_of_game.cheat_mode is True):
                        maze, adapter, drawing, ghosts = self.level_up(
                            pacman, waiting_ghosts)
                        in_game = InGame(screen, adapter)
                        level_timer = pygame.time.get_ticks()
                        continue

                    if event.key == pygame.K_q:
                        return "exit"
                    elif event.key in [pygame.K_DOWN, pygame.K_UP,
                                       pygame.K_LEFT, pygame.K_RIGHT]:
                        pacman.move.direction = diction_direction[event.key]

                    elif event.key == pygame.K_p:
                        state = pause_menu.run()
                        if state == "menu":
                            return state

            # ######################### update coords of pacman #############
            if pacman.move.frame == pacman.move.target:
                drawing.update_pacman_move(pacman, open_mouth)

            # ######################### take next frame to draw  ############
            pacman.current_frame = pacman.move.next_frame_x_y(pacman, dt)

            # ##################### super mode #################
            # this condition means im in super gum corner
            if (adapter.window_to_grad.get(pacman.current_frame, None) in
                    adapter.super_gums_positions):
                self.start_super_mode(pacman, ghosts)
                start_time_super = pygame.time.get_ticks()

            if pacman.super:
                self.check_mode_super_time(
                    pygame.time.get_ticks() - start_time_super, pacman, ghosts)

            # ######################### animate the ghosts  ##################
            ghosts_poses = []
            for i, ghost in enumerate(ghosts):
                ghosts_poses.append(ghost.move.next_frame_x_y(ghost, dt))

            # ######################### drawing player  #################
            drawing.draw_player(pacman)

            # ######################### drawing and respawn  #################

            for i, ghost_position in enumerate(ghosts_poses):
                drawing.draw_ghost(ghosts[i],
                                   adapter.window_to_grad.get(
                                       pacman.current_frame, None),
                                   ghost_position)

                if drawing.collusion(pacman.current_frame,
                                     ghosts[i].move.frame):

                    if pacman.time_after_respawning:
                        if (pygame.time.get_ticks() -
                           pacman.time_after_respawning) / 1000 <= 2:
                            continue

                    if pacman.super and ghosts[i].edible:
                        ghosts[i] = self.ghost_is_die(pacman,
                                                      ghosts[i], adapter)
                        waiting_ghosts.append(ghosts[i])

                    elif (pacman.data_of_game.cheat_mode is False and
                            not (pacman.super and ghosts[i].edible)):
                        self.pacman_is_die(pacman)

                ghosts_poses = []

            in_game.run(pacman.data_of_game, level_timer)
            if pacman.time_after_respawning:
                self.remove_imortale_mode_after_2s(pacman)

            pygame.display.flip()
            screen.fill((0, 0, 0))
        return None
