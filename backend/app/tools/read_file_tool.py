from langchain.tools import tool
from app.repositories import document_repository

@tool
def read_file_tool(conversation_id: int) -> str:

    """
    Read the entire uploaded document.

    Use when the user asks:
    - what is in the file
    - show the file
    - read the document
    - display document contents
    """
    global CURRENT_CONVERSATION_ID
    CURRENT_CONVERSATION_ID = conversation_id

   
    document = document_repository.get_document_by_conversation(CURRENT_CONVERSATION_ID)

    if not document:
        return "No document found."
     
    return document["raw_text"]