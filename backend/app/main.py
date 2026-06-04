from fastapi import FastAPI
from pydantic import BaseModel
from app.repositories import chat_repository

class ConversationCreate(BaseModel):
    title: str

class MessageCreate(BaseModel):
    conversation_id: int
    content: str

app = FastAPI()

# here @app is a decorator
@app.get("/")
def root():
    return {"message": "Chat API is running."}

@app.get("/conversations")
def get_conversations():
    return chat_repository.get_conversations()

@app.post("/conversations")
def create_conversations(body: ConversationCreate):
    return chat_repository.get_conversations(body.title)

@app.get("/conversations/{conversation_id}/messages")
def get_messages(conversation_id: int):
    return chat_repository.get_conversations(conversation_id)

@app.post("/messages")
def send_messages(body: MessageCreate):
    user_message = chat_repository.create_message(
        body.conversation_id, "user", body.content
    )
    assistant_message = chat_repository.create_message(
        body.conversation_id, "assistant", f"You said: {body.content}"
    )
    return {
        "user_message": user_message,
        "assistant_message": assistant_message
    }