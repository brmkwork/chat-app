from langchain.tools import tool
import traceback
from langchain_chroma import Chroma

from app.services.document_service import embeddings, CHROMA_DIR


@tool
def rag_search_tool(query: str) -> str:
    """
    Search a previously LOADED file (via load_file_tool) and return relevant chunks.

    Use this tool ONLY when:
      - the user asks a QUESTION about a file
      - the user wants a summary, analysis, or specific information extracted
      - the user asks "what does the file say about X?"

    DO NOT use this tool when the user simply wants to READ the file
    in full. For "read", "open", "show" requests, use read_file_tool.

    Returns retrieved text chunks from the file. The final answer
    to the user should be composed from these chunks.
    """

    try:
        vectorstore = Chroma(
            persist_directory=f"{CHROMA_DIR}/active_file",
            embedding_function=embeddings,
            collection_name="active_file",
        )

        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
        docs = retriever.invoke(query)

        if not docs:
            return "No relevant information found in the loaded file."

        return "\n\n".join(doc.page_content for doc in docs)

    except Exception as exc:
        traceback.print_exc()
        return f"RAG search failed: {str(exc)}"
