import os
import json
from typing import Any

class FileHandler:
    def __init__(self, file_path: str) -> None:
        self.file_path: str = file_path

    def load_json(self) -> dict[str, Any]:
        if not os.path.exists(self.file_path):
            return {}
        with open(self.file_path, 'r') as file:
            return json.load(file)

    def save_json(self, data: dict[str, Any]) -> None:
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def insert_to_json(self, key: str, value: Any) -> None:
        data: dict[str, Any] = self.load_json()
        data[key] = value
        self.save_json(data)

