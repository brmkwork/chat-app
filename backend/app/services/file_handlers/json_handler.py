import json

from .base_handler import BaseFileHandler

class JsonHandler(BaseFileHandler):

    def extract_text(self, file_path: str) -> str:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        return json.dumps(
            data,
            indent=2
        )