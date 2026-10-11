import json
from typing import List, Any, Dict


class DataBase:
    def __init__(self) -> None:
        self.file = "scores.json"

    def load_scores(self) -> list | Any:
        try:
            with open(self.file, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return []
        except PermissionError:
            raise ValueError("file mkhewer")

    def validate_scores(self, scores: List) -> List:

        if not isinstance(scores, list):
            return []

        valid_scores = []

        for entry in scores:
            if not isinstance(entry, dict):
                continue

            name = entry.get("name")
            score = entry.get("score")

            if not isinstance(name, str):
                continue

            if not isinstance(score, int) or isinstance(score, bool):
                continue

            if not name.strip() or len(name) > 10:
                continue

            if not all(char.isascii() and
                       (char.isalnum()) for char in name.strip()):
                continue

            if score < 0:
                continue

            valid_scores.append({
                "name": name,
                "score": score
            })

        return valid_scores

    def save_score(self, score: Dict) -> None:
        scores = self.validate_scores(self.load_scores())

        scores.append(score)
        try:
            with open(self.file, 'w') as file:
                json.dump(scores, file, indent=4)
        except Exception:
            raise ValueError("file mkhewer")

    def sorted_scores(self) -> List:
        scores = self.validate_scores(self.load_scores())
        return sorted(scores, key=lambda x: x["score"],
                      reverse=True)
