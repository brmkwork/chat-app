import os
from google import genai
from dotenv import load_dotenv
from app.repositories import chat_repository

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_conversations():
    return chat_repository.get_conversations()

def create_conversation(title: str):
    return chat_repository.create_conversation(title)

def get_messages(conversation_id: int):
    return chat_repository.get_messages(conversation_id)

def generate_response(content: str) -> str:
    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = content
    )

    return response.text

def send_message(conversation_id: int, content: str):
    user_message = chat_repository.create_message(
        conversation_id, "user", content
    )
    
    chat_repository.update_conversation(conversation_id, content)

    reply = generate_response(content)

    assistant_message = chat_repository.create_message(
        conversation_id, "assistant", reply
    )
    return {
        "user_message": user_message,
        "assistant_message": assistant_message
    }

def delete_conversation(conversation_id: int):
    return chat_repository.delete_conversation(conversation_id)