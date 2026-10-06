class GameData:
    def parser(file: str):
        pass

    def __init__(self):
        self.hearts = 3
        self.level = 1
        self.points_per_pacgum = 10
        self.points_per_superpacgum = 30
        self.points_per_ghost = 1000
        self.level_time = 5
        self.current_score = 0

    def ate_gum(self):
        self.current_score += self.points_per_pacgum

    def ate_supergum(self):
        self.current_score += self.points_per_superpacgum

    def ate_ghost(self):
        self.current_score += self.points_per_ghost
