import json
from typing import Any


class GameData:
    """ Tracking the game stats """

    def parser(self, file: str = "config.json") -> Any:
        """ Parse the provided file"""

        # need try except
        config = json.load(open(file))
        return config

    def __init__(self) -> None:
        """ Initialize the start stat data game """

        self.config = self.parser()
        self.hearts = self.config["hearts"]
        self.level = 1
        self.points_per_pacgum = self.config["points_per_pacgum"]
        self.points_per_superpacgum = self.config["points_per_superpacgum"]
        self.points_per_ghost = self.config["points_per_ghost"]
        self.level_time = self.config["level_time"]
        self.current_score = 0
        self.cheat_mode = self.config["cheat_mode"]

    def ate_gum(self) -> None:
        """ add the normal gum's points to the score"""

        self.current_score += self.points_per_pacgum

    def ate_supergum(self) -> None:
        """ add the super gum's points to the score"""

        self.current_score += self.points_per_superpacgum

    def ate_ghost(self) -> None:
        """ add the ghosts's points to the score"""

        self.current_score += self.points_per_ghost
