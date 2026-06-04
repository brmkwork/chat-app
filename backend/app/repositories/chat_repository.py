# This is a fake repository — no database yet.
# It returns hardcoded data so we can test the layer exists
# and is connected correctly before adding real database code.

fake_conversations = [
    {"id": 1, "title": "First chat"},
    {"id": 2, "title": "Second chat"},
]

fake_messages = [
    {"id": 1, "conversation_id": 1, "role": "user", "content": "Hello"},
    {"id": 2, "conversation_id": 1, "role": "assistant", "content": "You said: Hello"},
]

def get_conversations():
    return fake_conversations

def create_conversations(title:str):
    new = {"id":3, "title":title}
    return new

def get_messages(conversation_id: int):
    return [m for m in fake_messages if m["conversation_id"] == conversation_id]

def create_message(conversation_id: int, role: str, content: str):
    new = {
        "id": 99,
        "conversation_id": conversation_id,
        "role": role,
        "content": content
    }
    return new

