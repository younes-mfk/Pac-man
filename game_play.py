import pygame
from moves import Move
from UI import Pausemenu


class GamePlay:

    def run_the_gam(self, drawing, maze, adapter, ghosts, moved_ghosts,
                    screen, diction_direction, pacman):
        pause_menu = Pausemenu(
            screen,
            pygame.image.load("menu_images/pause_menu.png"),
            [pygame.image.load("menu_images/resume_game.png"),
             pygame.image.load("menu_images/return_menu.png")],
            [pygame.image.load("menu_images/selected_resume_game.png"),
             pygame.image.load("menu_images/selected_return_menu.png")])

        run = True
        clock = pygame.time.Clock()
        ghosts_poses = []
        start_time = None
        while run:

            open_mouth = (pygame.time.get_ticks() // 200) % 2
            r = clock.tick(100)
            dt = r / 1000

            # ########################## draw the basics #####################

            drawing.draw_map_and_gums(maze, adapter.gums_positions)

            # ########################## take orders #########################
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        run = False
                        return False
                    elif event.key in [pygame.K_DOWN, pygame.K_UP,
                                       pygame.K_LEFT, pygame.K_RIGHT]:
                        pacman.move.direction = diction_direction[event.key]
                    elif event.key == pygame.K_p:
                        state = pause_menu.run()
                        if state == "menu":
                            return state

            # ######################### animate the player  ##################

            if pacman.move.frame == pacman.move.target:
                drawing.update_pacman_move(pacman, open_mouth)

            pacman.current_frame = pacman.move.next_frame_x_y(pacman.move,
                                                              pacman.speed, dt)

            # ######################### animate the ghosts  ##################

            for i, ghost_move in enumerate(moved_ghosts):
                ghosts_poses.append(ghost_move.next_frame_x_y(ghost_move,
                                                              ghosts[i].speed,
                                                              dt))

            # ######################### drawing and respawn  #################

            drawing.draw_player(pacman.current_frame, pacman.move.image)

            for i, ghost_position in enumerate(ghosts_poses):
                moved_ghosts[i].current_pos, moved_ghosts[i].target = drawing.draw_ghost(ghosts[i], adapter.window_to_grad.get(pacman.current_frame, None), ghost_position)

                if drawing.collusion(pacman.current_frame, moved_ghosts[i].frame):
                    if start_time:
                        passed_time = pygame.time.get_ticks() - start_time
                        if passed_time / 1000 >= 2:
                            pacman.restart_move(pacman)
                            pacman.mortal = False
                            start_time = pygame.time.get_ticks()
                    else:
                        pacman.restart_move(pacman)
                        pacman.mortal = False
                        start_time = pygame.time.get_ticks()

                ghosts_poses = []

            if start_time:
                passed_time = pygame.time.get_ticks() - start_time
                if passed_time / 1000 >= 2:
                    pacman.mortal = True

            pygame.display.flip()
            screen.fill((0, 0, 0))
