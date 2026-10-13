"""Store, validate, and retrieve player scores using a JSON file."""

import json
from typing import List, Any, Dict


class DataBase:
    """Manage the persistent high scores stored in a JSON file"""

    def __init__(self) -> None:
        """Initialize the database with the default scores file.

        Args:
            file (str): Path of the JSON file holding the scores.

        """
        self.file = "scores.json"

    def load_scores(self) -> list | Any:
        """Read the raw scores from the JSON file.

        The content is returned as parsed, without validation. A
        missing or malformed file is treated as having no scores.

        Returns:
            list | Any: The data decoded from the file, or an empty
                list if the file does not exist or is not valid JSON.

        Raises:
            ValueError: If the file cannot be read because of missing
                permissions.
        """
        try:
            with open(self.file, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return []
        except PermissionError:
            raise ValueError("file cannot be read because of "
                             "missing permissions.")

    def validate_scores(self, scores: List) -> List:
        """Filter a list of scores, keeping only the valid entries.

        An entry is valid if it is a dictionary with a "name" and a
        "score" where:

        * the name is a string of at most ten characters, not blank,
          and made only of letters, digits, and spaces;
        * the score is a non-negative integer (booleans are rejected).

        Args:
            scores (List): The scores to validate, normally loaded from
                the file.

        Returns:
            List: A new list with the valid entries as dictionaries
                containing "name" and "score". An empty list is returned
                if the input is not a list.
        """

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

            if not all((char == ' ' or char.isalnum())
                       for char in name.strip()):
                continue

            if score < 0:
                continue

            valid_scores.append({
                "name": name,
                "score": score
            })

        return valid_scores

    def save_score(self, score: Dict) -> None:
        """Add a new score and write all scores back to the file.

        The existing scores are loaded and validated first, so invalid
        entries already in the file are discarded when saving.

        Args:
            score: The score to add, with the keys "name" (str)
                and "score" (int).

        Returns:
            None.

        Raises:
            ValueError: If the file cannot be written, or if reading
                the existing scores is not permitted.
        """
        scores = self.validate_scores(self.load_scores())

        scores.append(score)
        try:
            with open(self.file, 'w') as file:
                json.dump(scores, file, indent=4)
        except Exception:
            raise ValueError("file mkhewer")

    def sorted_scores(self) -> List:
        """Get the valid scores ordered from highest to lowest.

        Returns:
            List: Valid score dictionaries ("name" and "score") sorted
                by score in descending order.

        Raises:
            ValueError: If the scores file cannot be read because of
                missing permissions.
        """
        scores = self.validate_scores(self.load_scores())
        return sorted(scores, key=lambda x: x["score"],
                      reverse=True)
