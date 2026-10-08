import pygame
from UI import Pausemenu, InGame
from ghost_maker import GhostsMaker
import sys


class GamePlay:

    def start_super_mode(self, pacman, ghosts):
        pacman.super = True
        for ghost in ghosts:
            ghost.edible = True
            ghost.image = pygame.image.load("ghosts_images/ghost_yellow.png")

    def check_mode_super_time(self, passed_time_super, pacman, ghosts):
        if passed_time_super / 1000 >= 5:
            pacman.super = False

            for ghost in ghosts:
                ghost.image = pygame.image.load("ghosts_images/ghost.png")
                ghost.edible = False

    def check_pacman_is_alive(self, passed_time_game, pacman):
        if pacman.data_of_game.hearts == 0:
            print("WA METYY SIR TAWA")
            print("modifie rules from the file parse_config.py")
            sys.exit()

        if passed_time_game / 1000 > pacman.data_of_game.level_time:
            print("SALA LW9T SIR TAWA")
            print("modifie rules from the file parse_config.py")
            sys.exit()

    def level_up(self, pacman, adapter, ghosts):
        adapter.gums_positions = adapter.get_gums_positions(adapter.maze)[0]
        adapter.super_gums_positions = adapter.spawn_corners.copy()
        pacman.restart_move(pacman)
        pacman.reset_default_mode(pacman)
        pacman.data_of_game.level += 1
        pacman.data_of_game.hearts = 3

        ghosts_2 = []
        for ghost in ghosts:
            ghost.speed += 20
            ghosts_2.append(GhostsMaker.restart_ghost(ghost, adapter.grad_to_window, pacman.current_frame))
            ghosts = ghosts_2
        return ghosts_2, True

    def level_completed(self, pacman, adapter, ghosts):

        if len(adapter.gums_positions):
            return ghosts, False

        elif not len(adapter.gums_positions):
            return self.level_up(pacman, adapter, ghosts)

    def check_game_stat(self, pacman, adapter, ghosts, time_passed):
        self.check_pacman_is_alive(time_passed, pacman)
        ghosts, restart_timer = self.level_completed(pacman, adapter, ghosts)
        return ghosts, restart_timer

    def ghost_is_die(self, pacman, ghost, adapter):
        ghost = GhostsMaker.restart_ghost(ghost, adapter.grad_to_window, pacman.current_frame)
        pacman.data_of_game.ate_ghost()
        return ghost

    def pacman_is_die(self, pacman):
        pacman.data_of_game.hearts -= 1
        pacman.restart_move(pacman)
        pacman.mortal = False

    def run_the_gam(self, drawing, maze, adapter, ghosts,
                    screen, diction_direction, pacman):
        pause_menu = Pausemenu(screen)
        in_game = InGame(screen, adapter)
        run = True
        clock = pygame.time.Clock()
        ghosts_poses = []
        time_after_respawning = None
        timer = pygame.time.get_ticks()

        while run:

            if pacman.data_of_game.level == 10:
                print("YOU WIN")
                sys.exit()

            if pacman.data_of_game.cheat_mode is False:
                ghosts, restart_timer = self.check_game_stat(
                    pacman, adapter, ghosts, pygame.time.get_ticks() - timer)
                if restart_timer:
                    timer = pygame.time.get_ticks()
                    continue

            if pacman.data_of_game.cheat_mode is True and (pygame.time.get_ticks() - timer) / 1000 > 10:
                ghosts, restart_timer = self.level_up(pacman, adapter, ghosts)
                timer = pygame.time.get_ticks()
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
            pacman.current_frame = pacman.move.next_frame_x_y(pacman.move,
                                                              pacman.speed, dt)

            # ##################### super mode #################
            # this condition means im in super gum corner
            if adapter.window_to_grad.get(pacman.current_frame, None) in adapter.super_gums_positions:
                self.start_super_mode(pacman, ghosts)
                start_time_super = pygame.time.get_ticks()

            if pacman.super:
                self.check_mode_super_time(pygame.time.get_ticks() - start_time_super, pacman, ghosts)

            # ######################### animate the ghosts  ##################
            for i, ghost in enumerate(ghosts):
                ghosts_poses.append(ghost.move.next_frame_x_y(ghost.move,
                                                              ghost.speed,
                                                              dt))

            # ######################### drawing player  #################
            drawing.draw_player(pacman.current_frame, pacman.move.image, pacman)

            # ######################### drawing and respawn  #################

            for i, ghost_position in enumerate(ghosts_poses):
                drawing.draw_ghost(ghosts[i], adapter.window_to_grad.get(pacman.current_frame, None), ghost_position)

                if pacman.data_of_game.cheat_mode is False:
                    if drawing.collusion(pacman.current_frame, ghosts[i].move.frame):

                        if time_after_respawning:  # if he already die an the respawn mode start

                            passed_time = pygame.time.get_ticks() - time_after_respawning

                            if passed_time / 1000 >= 2:  # if 2 seconds are passed

                                if pacman.super and ghosts[i].edible:  # pacman win
                                    ghosts[i] = self.ghost_is_die(pacman, ghosts[i], adapter)
                                else:  # ghost win
                                    self.pacman_is_die(pacman)
                                    time_after_respawning = pygame.time.get_ticks()

                        else:  # the tine is None in the first time you respawned bcs you in normal mode directly

                            if pacman.super and ghosts[i].edible:  # pacman win
                                ghosts[i] = self.ghost_is_die(pacman, ghosts[i], adapter)

                            else:  # ghost win
                                self.pacman_is_die(pacman)
                                time_after_respawning = pygame.time.get_ticks()

                ghosts_poses = []

            in_game.run(pacman.data_of_game, timer)

            if time_after_respawning:  # to remove the imortal mode after 2s of respawnin
                passed_time = pygame.time.get_ticks() - time_after_respawning
                if passed_time / 1000 >= 2:
                    pacman.mortal = True

            pygame.display.flip()
            screen.fill((0, 0, 0))
