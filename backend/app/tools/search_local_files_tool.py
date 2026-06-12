from langchain.tools import tool
from app.services.local_file_service import search_files


@tool
def search_local_files_tool(query: str) -> str:
    """
    Search local machine files by filename.

    Use when user asks:
    - find file
    - locate file
    - search for file
    """

    results = search_files(query)

    if not results:
        return "No matching files found."

    return "\n".join(results)