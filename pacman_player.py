from moves import Move
from parse_config import GameData
from typing import Tuple, Dict


class PacMan:
    """Represent the Pacman player and controle its state"""

    def __init__(self, start_pos: Tuple, parsed_config: Dict) -> None:
        """Initialize Pacman at the starting position and more infos

        Args:
            start_pos: the initial position of pacman
        """
        self.speed = 470
        self.start_pos = start_pos
        self.current_frame = start_pos

        self.move = Move(start_pos, start_pos,
                         float(start_pos[0]),
                         float(start_pos[1]),
                         start_pos)
        self.super = False
        self.mortal = True
        self.data_of_game = GameData(parsed_config)
        self.time_after_respawning: None | float = None

    def restart_move(self, pacman: "PacMan") -> None:
        """Reset Pacman movement to its starting position

        Args:
            pacman: the pacman obj
        """

        pacman.move = Move(pacman.start_pos,
                           pacman.start_pos,
                           float(pacman.start_pos[0]),
                           float(pacman.start_pos[1]),
                           pacman.start_pos)

        pacman.current_frame = pacman.start_pos

    def reset_default_mode(self, pacman: "PacMan") -> None:
        """Restore pacman default modes

        Args:
            pacman: The pacman obj
        """

        pacman.super = False
        pacman.mortal = True

    def new_level(self, start_pos: Tuple) -> None:
        """reset pacman starting position for a new level
        Args:
            start_pos: The starting position in the new level
        """
        self.start_pos = start_pos
        self.restart_move(self)
        self.reset_default_mode(self)
        self.time_after_respawning = None
