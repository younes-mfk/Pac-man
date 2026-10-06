import pygame


class Move:
    pacman = [pygame.image.load("images/pacman_player_right_open.png"),
              pygame.image.load("images/pacman_player_left_open.png"),
              pygame.image.load("images/pacman_player_down_open.png"),
              pygame.image.load("images/pacman_player_up_open.png"),

              pygame.image.load("images/pacman_closed_right_close.png"),
              pygame.image.load("images/pacman_closed_left_close.png"),
              pygame.image.load("images/pacman_closed_down_close.png"),
              pygame.image.load("images/pacman_closed_up_close.png"),

              pygame.image.load("images/pacman_open_right_transparent.png"),
              pygame.image.load("images/pacman_open_left_transparent.png"),
              pygame.image.load("images/pacman_open_down_transparent.png"),
              pygame.image.load("images/pacman_open_up_transparent.png"),

              pygame.image.load("images/pacman_closed_right_transparent.png"),
              pygame.image.load("images/pacman_closed_left_transparent.png"),
              pygame.image.load("images/pacman_closed_down_transparent.png"),
              pygame.image.load("images/pacman_closed_up_transparent.png")
              ]

    respawn_images = {
        "r": [pacman[8], pacman[12]],
        "l": [pacman[9], pacman[13]],
        "d": [pacman[10], pacman[14]],
        "u": [pacman[11], pacman[15]],
        "": [pacman[11], pacman[15]]
    }

    images = {
        "r": [pacman[0], pacman[4]],
        "l": [pacman[1], pacman[5]],
        "d": [pacman[2], pacman[6]],
        "u": [pacman[3], pacman[7]],
        "": [pacman[3], pacman[7]],
    }

    def __init__(self, current_pos, next_pos, current_frame_pos_x,
                 current_frame_pos_y, frame):

        self.current_pos = current_pos
        self.target = next_pos
        self.current_frame_x = current_frame_pos_x
        self.current_frame_y = current_frame_pos_y
        self.direction = ""
        self.axis = ""
        self.frame = frame
        self.koller = True

    def next_frame(self, current_z, target_z, speed, dt):
        returned = current_z

        if current_z < target_z:
            returned += speed * dt
            if returned > target_z:
                returned = target_z

        elif current_z > target_z:
            returned -= speed * dt
            if returned < target_z:
                returned = target_z

        return returned

    def next_frame_x_y(self, move, speed, dt):

        move.current_frame_x = self.next_frame(move.current_frame_x,
                                               move.target[0], speed, dt)

        move.current_frame_y = self.next_frame(move.current_frame_y,
                                               move.target[1], speed, dt)

        player_position = (round(move.current_frame_x),
                           round(move.current_frame_y))
        move.frame = player_position
        return player_position
