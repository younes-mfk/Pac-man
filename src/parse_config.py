from typing import Dict


class GameData:
    """ Tracking the game stats """

    def __init__(self, parsed_config: Dict) -> None:
        """ Initialize the start stat data game
         Args:
            parsed_config: the parsed dict from config file
        """

        self.config = parsed_config
        self.hearts = self.config.get("hearts", 3)
        self.level = 1
        self.points_per_pacgum = self.config.get("points_per_pacgum", 10)
        self.points_per_superpacgum = self.config.get(
                                        "points_per_superpacgum", 10)
        self.points_per_ghost = self.config.get("points_per_ghost", 10)
        self.level_time = self.config.get("level_time", 90)
        self.current_score = 0
        self.cheat_mode = self.config.get("cheat_mode", False)

    def ate_gum(self) -> None:
        """ add the normal gum's points to the score"""

        self.current_score += self.points_per_pacgum

    def ate_supergum(self) -> None:
        """ add the super gum's points to the score"""

        self.current_score += self.points_per_superpacgum

    def ate_ghost(self) -> None:
        """ add the ghosts's points to the score"""

        self.current_score += self.points_per_ghost
