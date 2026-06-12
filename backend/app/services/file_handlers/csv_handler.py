import pandas as pd

from .base_handler import BaseFileHandler

class CsvHandler(BaseFileHandler):

    def extract_text(self, file_path: str) -> str:

        df = pd.read_csv(file_path)

        return df.to_string(index=False)