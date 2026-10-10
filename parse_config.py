import json


class GameData:

    def parser(file: str = "config.json"):
        # need try except
        config = json.load(open("config.json"))
        return config

    def __init__(self):
        self.config = self.parser()
        self.hearts = self.config["hearts"]
        self.level = 1
        self.points_per_pacgum = self.config["points_per_pacgum"]
        self.points_per_superpacgum = self.config["points_per_superpacgum"]
        self.points_per_ghost = self.config["points_per_ghost"]
        self.level_time = self.config["level_time"]
        self.current_score = 0
        self.cheat_mode = self.config["cheat_mode"]

    def ate_gum(self):
        self.current_score += self.points_per_pacgum

    def ate_supergum(self):
        self.current_score += self.points_per_superpacgum

    def ate_ghost(self):
        self.current_score += self.points_per_ghost
