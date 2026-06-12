from .base_handler import BaseFileHandler

class TxtHandler(BaseFileHandler):

    def extract_text(self, file_path: str) -> str:
        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as f:
            return f.read()