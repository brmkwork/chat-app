from app.repositories import chat_repository

def get_conversations():
    return chat_repository.get_conversations()

def create_conversations(title: str):
    return chat_repository.create_conversations(title)

def get_messages(conversation_id: int, content: str):
    return chat_repository.get_messages(conversation_id)

def send_messages(conversation_id: int, content: str):
    user_message = chat_repository.create_message(
        conversation_id, "user", content
    )
    assistant_message = chat_repository.create_message(
        conversation_id, "assistant", f"You said: {content}"
    )
    return {
        "user_message": user_message,
        "assistant_message": assistant_message
    }