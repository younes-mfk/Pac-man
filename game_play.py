import pygame
from moves import Move


class GamePlay:

    def run_the_gam(self, drawing, maze, adapter, ghosts, moved_ghosts, move_player, screen, diction_direction):
        run = True
        clock = pygame.time.Clock()
        ghosts_poses = []
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
                    elif event.key in [pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT]:
                        move_player.direction = diction_direction[event.key]

            # ######################### animate the player  ##################

            if move_player.frame == move_player.target:
                drawing.update_pacman_move(move_player, open_mouth)

            player_position = move_player.next_frame_x_y(move_player, adapter.speed, dt)

            # ######################### animate the ghosts  ##################

            for i, ghost_move in enumerate(moved_ghosts):
                ghosts_poses.append(ghost_move.next_frame_x_y(ghost_move, ghosts[i].speed, dt))

            # ######################### drawing and respawn  #################

            drawing.draw_player(player_position, move_player.image)

            for i, ghost_position in enumerate(ghosts_poses):
                moved_ghosts[i].current_pos, moved_ghosts[i].target = drawing.draw_ghost(ghosts[i], adapter.window_to_grad.get(player_position, None), ghost_position)

                if drawing.is_colliding(move_player.frame, moved_ghosts[i].frame):
                    move_player = Move(adapter.player_position, adapter.player_position, float(adapter.player_position_x), float(adapter.player_position_y), adapter.player_position)
                ghosts_poses = []

            pygame.display.flip()
            screen.fill((0, 0, 0))
