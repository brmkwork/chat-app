from fastapi import FastAPI
from pydantic import BaseModel
from app.services import chat_service

app = FastAPI()

class ConversationCreate(BaseModel):
    title: str

class MessageCreate(BaseModel):
    conversation_id: int
    content: str


@app.get("/")
def root():
    return {"message": "Chat API is running"}


@app.get("/conversations")
def get_conversations():
    return chat_service.get_conversations()


@app.post("/conversations")
def create_conversation(body: ConversationCreate):
    return chat_service.create_conversation(body.title)


@app.get("/conversations/{conversation_id}/messages")
def get_messages(conversation_id: int):
    return chat_service.get_messages(conversation_id)


@app.post("/messages")
def send_message(body: MessageCreate):
    return chat_service.send_message(body.conversation_id, body.content)