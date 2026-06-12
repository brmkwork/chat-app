import fitz
import logging

from .base_handler import BaseFileHandler
logger = logging.getLogger(__name__)

class PdfHandler(BaseFileHandler):

    def extract_text(self, file_path):
        logger.info(
            "PdfHandler -> extracting text from %s",
            file_path
        )

        doc = fitz.open(file_path)
        text = ""

        for page_number, page in enumerate(doc):

            logger.debug(
                "PdfHandler -> processing page %s",
                page_number + 1
            )

            text += page.get_text()
        doc.close()

        logger.info(
            "PdfHandler -> extracted %s characters",
            len(text)
        )

        return text