import logging
import os
import groq
from dotenv import load_dotenv
from app.repositories import chat_repository
from app.services import document_service

load_dotenv()

api_key = os.getenv("GROQ_API_KEY") or os.getenv("GEMINI_API_KEY")
logger = logging.getLogger(__name__)
client = groq.Groq(api_key=api_key)

def get_conversations():
    return chat_repository.get_conversations()

def create_conversation(title: str):
    return chat_repository.create_conversation(title)

def get_messages(conversation_id: int):
    return chat_repository.get_messages(conversation_id)


def truncate_context(context: str, max_chars: int = 3000) -> str:
    if len(context) <= max_chars:
        return context

    truncated = context[:max_chars]
    boundary = truncated.rfind("\n\n")
    if boundary > 0:
        truncated = truncated[:boundary]
    return truncated


def generate_response(conversation_id: int, content: str) -> tuple[str, dict]:
    context = document_service.get_relevant_chunks(conversation_id, content, max_chunks=6)
    context = truncate_context(context, max_chars=3000)

    if context:
        user_prompt = (
            "You are a retrieval-augmented assistant. Use the DOCUMENT CONTEXT below as the primary source to answer.\n"
            "If the question can be answered directly from the document, answer using that information.\n"
            "Do not invent unsupported facts.\n"
            "If the answer is not clearly supported by the provided document context, respond with: "
            "\"I cannot answer confidently from the provided document context.\"\n\n"
            "DOCUMENT CONTEXT:\n"
            f"{context}\n\n"
            "QUESTION:\n"
            f"{content}\n\n"
            "Provide a concise, direct answer in plain text only."
        )
    else:
        user_prompt = (
            "You are a concise assistant. There is no document context available.\n"
            "Answer the user using only your general knowledge.\n\n"
            "QUESTION:\n"
            f"{content}\n\n"
            "Provide a concise, direct answer in plain text only."
        )

    logger.debug("Retrieved document context for conversation %s: %s", conversation_id, context[:1000])

    response = client.chat.completions.create(
        model="compound-beta",
        messages=[
            {"role": "system", "content": "You are a retrieval-augmented assistant. Prefer the provided document context and avoid unsupported claims."},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=512,
        temperature=0.4,
    )

    answer = ""
    if getattr(response, "choices", None):
        first_choice = response.choices[0]
        answer = getattr(first_choice.message, "content", "") or ""

    metadata = {
        "response_id": getattr(response, "id", None),
        "model": getattr(response, "model", None),
        "finish_reason": getattr(first_choice, "finish_reason", None) if getattr(response, "choices", None) else None,
        "total_tokens": getattr(response.usage, "total_tokens", None) if getattr(response, "usage", None) else None,
        "prompt_tokens": getattr(response.usage, "prompt_tokens", None) if getattr(response, "usage", None) else None,
        "completion_tokens": getattr(response.usage, "completion_tokens", None) if getattr(response, "usage", None) else None,
        "groq_request_id": getattr(getattr(response, "x_groq", None), "id", None),
        "text_length": len(answer),
    }

    logger.info(
        "Groq response: id=%s model=%s finish_reason=%s total_tokens=%s prompt_tokens=%s completion_tokens=%s text_length=%s",
        metadata["response_id"],
        metadata["model"],
        metadata["finish_reason"],
        metadata["total_tokens"],
        metadata["prompt_tokens"],
        metadata["completion_tokens"],
        metadata["text_length"],
    )
    logger.debug("Groq answer: %s", answer)

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