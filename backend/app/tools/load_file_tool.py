import os
import shutil
import logging

from langchain.tools import tool
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from app.services.document_service import embeddings, CHROMA_DIR
from app.services.file_handlers.file_manager import FileManager

logger = logging.getLogger(__name__)

file_manager = FileManager()


@tool
def load_file_tool(file_path: str) -> str:
    """
    Load a file into the vector database so it can be queried with rag_search_tool.

    This is a SETUP step. It does NOT answer questions by itself.
    After calling this tool, you MUST call rag_search_tool to answer the user's question.

    Use this tool ONLY when the user asks a QUESTION about a file
    (e.g. "what does it say about X?", "summarize", "find mentions of Y").
    DO NOT use this tool when the user simply wants to READ the file —
    in that case use read_file_tool instead.
    """

    if not os.path.isfile(file_path):
        return (
            "Invalid file path. Please provide an existing local file path "
            "for the file you want to load."
        )

    try:
        text, file_type, handler_used = file_manager.extract_text(file_path)
    except Exception as exc:
        logger.error("LOAD_FILE_TOOL failed: %s", exc)
        return f"Failed to load file: {exc}"

    logger.info(
        "LOAD_FILE_TOOL -> handler=%s type=%s length=%d",
        handler_used,
        file_type,
        len(text),
    )

    persist_dir = f"{CHROMA_DIR}/active_file"

    if os.path.exists(persist_dir):
        shutil.rmtree(persist_dir)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )

    chunks = splitter.split_text(text)

    Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        persist_directory=persist_dir,
        collection_name="active_file",
    )

    return (
        f"File loaded into vector store.\n"
        f"Handler: {handler_used}\n"
        f"Chunks: {len(chunks)}\n"
        f"Next step: call rag_search_tool with the user's question."
    )
