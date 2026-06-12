from langchain.tools import tool
from app.services import document_service


@tool
def rag_search_tool(
    conversation_id: int,
    query: str
) -> str:
    """
    Search the uploaded document for information
    relevant to the user's question.
    """
    global CURRENT_CONVERSATION_ID

    CURRENT_CONVERSATION_ID = conversation_id
    
    

    return document_service.get_relevant_chunks(
        CURRENT_CONVERSATION_ID,
        query
    )