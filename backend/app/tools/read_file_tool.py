from langchain.tools import tool
from app.services.file_handlers.file_manager import FileManager
import logging

logger = logging.getLogger(__name__)

file_manager = FileManager()


@tool(return_direct=True)
def read_file_tool(file_path: str) -> str:
    """
    Return the COMPLETE, RAW contents of a file. No summarization. No analysis.

    Use this tool ONLY when the user explicitly asks to:
      - "read" a file
      - "open" a file
      - "show" a file
      - "display" a file
      - "print" a file
      - "give me" / "show me" the contents of a file
      - "what is in" a file (when they want the full text, not an answer)

    DO NOT use this tool when the user asks a QUESTION about a file
    (e.g. "what skills are mentioned?", "summarize", "explain", "how many...").
    For questions, use load_file_tool followed by rag_search_tool instead.

    Returns the entire file content as a single string.
    """

    text, file_type, handler_used = file_manager.extract_text(file_path)

    logger.info(
        "READ_FILE_TOOL -> handler=%s type=%s length=%d",
        handler_used,
        file_type,
        len(text),
    )

    # Return raw text. Do NOT add commentary. Do NOT summarize.
    return text
