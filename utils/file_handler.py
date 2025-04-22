import os
import json
from typing import Any


class FileHandler:
    FILE_PATH = "checklist.json"

    @staticmethod
    def load_json() -> list[dict[str, Any]]:
        if not os.path.exists(FileHandler.FILE_PATH):
            return []
        with open(FileHandler.FILE_PATH, "r") as file:
            return json.load(file)

    @staticmethod
    def save_json(data: list[dict[str, Any]]) -> None:
        with open(FileHandler.FILE_PATH, "w") as file:
            json.dump(data, file, indent=4)
