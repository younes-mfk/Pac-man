import json


class DataBase:
    def __init__(self) -> None:
        self.file = "scores.json"

    def load_scores(self):
        try:
            with open(self.file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []
        except (PermissionError, json.decoder.JSONDecodeError):
            raise ValueError("file mkhewer")

    def save_score(self, score):
        scores = self.load_scores()
        scores.append(score)
        try:
            with open(self.file, 'w') as file:
                json.dump(scores, file, indent=4)
        except Exception:
            raise ValueError("file mkhewer")

    def sorted_scores(self):
        return sorted(self.load_scores(), key=lambda x: x["score"],
                      reverse=True)
