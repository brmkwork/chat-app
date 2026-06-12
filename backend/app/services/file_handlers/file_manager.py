import os
import logging
from .txt_handler import TxtHandler
from .md_handler import MarkdownHandler
from .csv_handler import CsvHandler
from .json_handler import JsonHandler
from .docx_handler import DocxHandler

from .pdf_handler import PdfHandler
logger = logging.getLogger(__name__)

class FileManager:

    def __init__(self):

        self.handlers = {
        ".pdf": PdfHandler(),
        ".txt": TxtHandler(),
        ".md": MarkdownHandler(),
        ".csv": CsvHandler(),
        ".json": JsonHandler(),
        ".docx": DocxHandler(),
}

    def extract_text(
            self, 
            file_path: str
    ) -> tuple[str, str, str]:
        
        extension = os.path.splitext(
            file_path
        )[1].lower()

        logger.info(
            "FileManager -> detected extension %s",
            extension
        )

        handler = self.handlers.get(extension)
        if not handler:

            logger.error(
                "FileManager -> unsupported file type %s",
                extension
            )

            raise ValueError(
                f"Unsupported file type: {extension}"
            )

        logger.info(
            "FileManager -> selected handler %s",
            handler.__class__.__name__
        )

        text = handler.extract_text(
            file_path
        )

        return (
            text,
            extension,
            handler.__class__.__name__
        )
