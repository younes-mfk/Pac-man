import pygame
from UI import Pausemenu, InGame
from ghost_maker import GhostsMaker


diction_direction = {
        pygame.K_RIGHT: "r",
        pygame.K_LEFT: "l",
        pygame.K_UP: "u",
        pygame.K_DOWN: "d"}


class GamePlay:

    def __init__(self, level_factory):
        self.level_factory = level_factory

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
            return "game over"

        if passed_time_game / 1000 > pacman.data_of_game.level_time:
            return "game over"

        return None

    def respawning_died_ghosts_after_3s(self, waiting_ghosts, ghosts, force=False):
        if force:
            for ghost in (waiting_ghosts[:]):
                ghosts.append(ghost)
                waiting_ghosts.remove(ghost)
        else:
            for ghost in (waiting_ghosts[:]):
                if (pygame.time.get_ticks() - ghost.respawning_time) // 1000 >= 3:
                    ghosts.append(ghost)
                    waiting_ghosts.remove(ghost)

    def level_up(self, pacman, waiting_ghosts):
        pacman.data_of_game.level += 1
        level = self.level_factory.create(pacman.data_of_game.level, 0)
        pacman.new_level(level.adapter.player_position)
        waiting_ghosts.clear()
        return (level.maze, level.adapter, level.drawing, level.ghosts)

    def level_completed(self, adapter):
        return not len(adapter.gums_positions)

    def check_game_stat(self, pacman, adapter, time_passed):
        state = self.check_pacman_is_alive(time_passed, pacman)
        if state:
            return state

        if self.level_completed(adapter):
            return "level up"

        return None

    def ghost_is_die(self, pacman, ghost, adapter):
        ghost = GhostsMaker.restart_ghost(ghost, adapter.grad_to_window,
                                          pacman.current_frame)
        ghost.respawning_time = pygame.time.get_ticks()

        pacman.data_of_game.ate_ghost()
        return ghost

    def pacman_is_die(self, pacman):
        pacman.data_of_game.hearts -= 1
        pacman.restart_move(pacman)
        pacman.mortal = False
        pacman.time_after_respawning = pygame.time.get_ticks()

    def died_or_win(self, adapter, pacman, time_down_of_level):
        return self.check_game_stat(pacman, adapter, time_down_of_level)

    def remove_waiting_ghosts_from_ghosts_list(self, waiting_ghosts, ghosts):
        for ghost in waiting_ghosts:
            if ghost in ghosts:
                ghosts.remove(ghost)

    def remove_imortale_mode_after_2s(self, pacman):
        if pacman.time_after_respawning:
            passed_time = pygame.time.get_ticks() - pacman.time_after_respawning
            if passed_time / 1000 >= 2:
                pacman.mortal = True

    def you_win(self, pacman):
        if pacman.data_of_game.level == 10:
            print("YOU WIN")
            return True
        else:
            return None

    def run_the_gam(self, drawing, maze, adapter, ghosts,
                    screen, pacman):
        pause_menu = Pausemenu(screen)
        in_game = InGame(screen, adapter)
        run = True
        clock = pygame.time.Clock()
        level_timer = pygame.time.get_ticks()
        waiting_ghosts = []

        while run:
            self.remove_waiting_ghosts_from_ghosts_list(waiting_ghosts, ghosts)
            self.respawning_died_ghosts_after_3s(waiting_ghosts, ghosts)
            if self.you_win(pacman):
                return "victory"

            # ################## you in competetive mode ###############
            time_in_level = pygame.time.get_ticks() - level_timer

            if pacman.data_of_game.cheat_mode is False:
                state = self.died_or_win(adapter, pacman, time_in_level)
            elif time_in_level / 1000 > 10:
                state = "level up"
            else:
                state = None

            if state == "game over":
                return state

            if state == "level up":
                maze, adapter, drawing, ghosts = self.level_up(pacman, waiting_ghosts)
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
                self.check_mode_super_time(pygame.time.get_ticks() - start_time_super, pacman, ghosts)

            # ######################### animate the ghosts  ##################
            ghosts_poses = []
            for i, ghost in enumerate(ghosts):
                ghosts_poses.append(ghost.move.next_frame_x_y(ghost, dt))

            # ######################### drawing player  #################
            drawing.draw_player(pacman)

            # ######################### drawing and respawn  #################

            for i, ghost_position in enumerate(ghosts_poses):
                drawing.draw_ghost(ghosts[i], adapter.window_to_grad.get(pacman.current_frame, None), ghost_position)

                if pacman.data_of_game.cheat_mode is False:
                    if drawing.collusion(pacman.current_frame, ghosts[i].move.frame):

                        if pacman.time_after_respawning:
                            if (pygame.time.get_ticks() - pacman.time_after_respawning) / 1000 < 2:
                                continue

                        if pacman.super and ghosts[i].edible:
                            ghosts[i] = self.ghost_is_die(pacman, ghosts[i], adapter)
                            waiting_ghosts.append(ghosts[i])

                        else:
                            self.pacman_is_die(pacman)

                ghosts_poses = []

            in_game.run(pacman.data_of_game, level_timer)

            if pacman.time_after_respawning:
                self.remove_imortale_mode_after_2s(pacman)

            pygame.display.flip()
            screen.fill((0, 0, 0))
