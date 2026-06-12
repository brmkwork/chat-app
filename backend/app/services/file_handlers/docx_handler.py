from docx import Document

from .base_handler import BaseFileHandler

class DocxHandler(BaseFileHandler):

    def extract_text(
        self,
        file_path: str
    ) -> str:

        doc = Document(file_path)

        return "\n".join(
            p.text
            for p in doc.paragraphs
        )