import logging
import os
from dotenv import load_dotenv
from app.repositories import chat_repository
from app.services import document_service
from langchain.chat_models import init_chat_model
from app.services.agent_service import ask_agent

load_dotenv()

logger = logging.getLogger(__name__)


def get_conversations():
    return chat_repository.get_conversations()


def create_conversation(title: str):
    return chat_repository.create_conversation(title)


def get_messages(conversation_id: int):
    return chat_repository.get_messages(conversation_id)


# def generate_response(conversation_id: int, content: str) -> tuple[str, dict]:
#     llm = init_chat_model(
#         "groq:llama-3.3-70b-versatile",
#         temperature=0.4,
#         api_key=os.getenv("GROQ_API_KEY"),
#     )

#     try:
#         vectorstore = document_service.get_vectorstore(conversation_id)
#         retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
#         docs = retriever.invoke(content)
#         context = "\n\n".join(getattr(d, "page_content", "") for d in docs)
#         context = context[:2000]
#     except Exception as exc:
#         logger.warning("Retrieval failed: %s", exc)
#         context = ""

#     if context:
#         prompt = (
#             "You are a retrieval augmented assistant.\n"
#             "Use the supplied context to answer.\n"
#             "If the answer is not in the context, say you do not know.\n\n"
#             f"Context:\n{context}\n\n"
#             f"Question: {content}\n\nAnswer:"
#         )
#     else:
#         prompt = (
#             "You are a helpful assistant.\n"
#             f"Question: {content}\n\nAnswer:"
#         )

#     messages = [
#         ("system", "You are a retrieval augmented assistant."),
#         ("human", prompt),
#     ]

#     ai_response = llm.invoke(messages)
#     answer = ai_response.content if hasattr(ai_response, "content") else str(ai_response)

#     metadata = {"model": "llama-3.3-70b-versatile", "retriever_k": 3}
#     return answer, metadata

def generate_response(
    conversation_id: int,
    content: str
) -> tuple[str, dict]:

    answer = ask_agent(
        conversation_id,
        content
    )

    metadata = {
        "agent": True
    }

    return answer, metadata

def send_message(conversation_id: int, content: str):
    user_message = chat_repository.create_message(
        conversation_id, "user", content
    )

    chat_repository.update_conversation(conversation_id, content)

    reply, metadata = generate_response(conversation_id, content)

    assistant_message = chat_repository.create_message(
        conversation_id, "assistant", reply
    )
    return {
        "user_message": user_message,
        "assistant_message": assistant_message,
        "groq_metadata": metadata,
    }


def delete_conversation(conversation_id: int):
    return chat_repository.delete_conversation(conversation_id)