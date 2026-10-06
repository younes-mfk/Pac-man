from moves import Move
from parse_config import GameData
import sys


class PacMan:
    def __init__(self, start_pos, speed=470):
        self.speed = speed
        self.start_pos = start_pos
        self.current_frame = start_pos

        self.mortal = True
        self.move = Move(start_pos, start_pos,
                         float(start_pos[0]),
                         float(start_pos[1]),
                         start_pos)
        self.super = False
        self.data_of_game = GameData()

    def restart_move(self, pacman):
        pacman.move = Move(pacman.start_pos,
                           pacman.start_pos,
                           float(pacman.start_pos[0]),
                           float(pacman.start_pos[1]),
                           pacman.start_pos)

        pacman.current_frame = pacman.start_pos

    def pacman_is_alive(self, passed_time_game):
        if self.data_of_game.hearts == 0:
            print("WA METYY SIR TAWA")
            print("modifie rules from the file parse_config.py")
            sys.exit()

        if passed_time_game / 1000 > self.data_of_game.level_time:
            print("SALA LW9T SIR TAWA")
            print("modifie rules from the file parse_config.py")
            sys.exit()

        print(" score : ", end=" ")
        print(self.data_of_game.current_score, end=" | ")
        print(" hearts : ", end=" ")
        print(self.data_of_game.hearts, end=" | ")
        print(" level : ", end=" ")
        print(self.data_of_game.level, end=" | ")
        print(" time passed : ", end=" ")
        print(round(self.data_of_game.level_time - passed_time_game/1000))
