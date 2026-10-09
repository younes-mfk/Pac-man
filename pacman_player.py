from moves import Move
from parse_config import GameData


class PacMan:
    def __init__(self, start_pos, speed=470):
        self.speed = speed
        self.start_pos = start_pos
        self.current_frame = start_pos

        self.move = Move(start_pos, start_pos,
                         float(start_pos[0]),
                         float(start_pos[1]),
                         start_pos)
        self.super = False
        self.mortal = True
        self.data_of_game = GameData()
        self.time_after_respawning = None

    def restart_move(self, pacman):
        pacman.move = Move(pacman.start_pos,
                           pacman.start_pos,
                           float(pacman.start_pos[0]),
                           float(pacman.start_pos[1]),
                           pacman.start_pos)

        pacman.current_frame = pacman.start_pos

    def reset_default_mode(self, pacman):
        pacman.super = False
        pacman.mortal = True
