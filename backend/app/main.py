import os
import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.services import chat_service
from app.database.db import engine, Base
from app.models import conversation, message

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

class ConversationCreate(BaseModel):
    title: str

class MessageCreate(BaseModel):
    conversation_id: int
    content: str

@app.get("/")
def root():
    return {"message": "Chat API is running"}

@app.get("/debug/db-status")
def db_status():
    db_path = os.path.abspath("./chat.db")
    counts = {}
    try:
        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()
            for table in ["conversations", "messages"]:
                cur.execute(f"SELECT count(*) FROM {table}")
                counts[table] = cur.fetchone()[0]
    except Exception as e:
        return {"db_path": db_path, "error": str(e)}

    return {"db_path": db_path, "counts": counts}


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


@app.delete("/conversations/{conversation_id}")
def delete_conversation(conversation_id: int):
    result = chat_service.delete_conversation(conversation_id)
    if result is None:
        return {"deleted": False}
    return {"deleted": True, "id": conversation_id}