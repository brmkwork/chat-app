from app.repositories import chat_repository

def get_conversations():
    return chat_repository.get_conversations()

def create_conversation(title: str):
    return chat_repository.create_conversation(title)

def get_messages(conversation_id: int):
    return chat_repository.get_messages(conversation_id)

def send_message(conversation_id: int, content: str):
    user_message = chat_repository.create_message(
        conversation_id, "user", content
    )
    assistant_message = chat_repository.create_message(
        conversation_id, "assistant", "Message Received"
    )
    return {
        "user_message": user_message,
        "assistant_message": assistant_message
    }

def delete_conversation(conversation_id: int):
    return chat_repository.delete_conversation(conversation_id)