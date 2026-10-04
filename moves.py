import pygame


class Move:
    pacman = [pygame.image.load("images/pacman_player_right_open.png"),
              pygame.image.load("images/pacman_player_left_open.png"),
              pygame.image.load("images/pacman_player_down_open.png"),
              pygame.image.load("images/pacman_player_up_open.png"),
              pygame.image.load("images/pacman_closed_right_close.png"),
              pygame.image.load("images/pacman_closed_left_close.png"),
              pygame.image.load("images/pacman_closed_down_close.png"),
              pygame.image.load("images/pacman_closed_up_close.png")
              ]

    images = {
        "r": [pacman[0], pacman[4]],
        "l": [pacman[1], pacman[5]],
        "d": [pacman[2], pacman[6]],
        "u": [pacman[3], pacman[7]],
        "": [pacman[3], pacman[7]],
    }

    def __init__(self, current_pos, next_pos, current_frame_pos_x, current_frame_pos_y):
        self.current_pos = current_pos
        self.target = next_pos
        self.current_frame_x = current_frame_pos_x
        self.current_frame_y = current_frame_pos_y
        self.direction = ""
        self.axis = ""
        self.image = pygame.image.load("images/pacman_closed_up_close.png")
        self.image_ghost = pygame.image.load("ghosts_images/ghost.png")
