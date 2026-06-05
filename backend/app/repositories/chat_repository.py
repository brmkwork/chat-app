from app.database.db import SessionLocal
from app.models.conversation import Conversation
from app.models.message import Message


def serialize_conversation(conv: Conversation) -> dict:
    return {
        "id": conv.id,
        "title": conv.title,
        "created_at": conv.created_at.isoformat() if conv.created_at else None,
    }


def serialize_message(msg: Message) -> dict:
    return {
        "id": msg.id,
        "conversation_id": msg.conversation_id,
        "role": msg.role,
        "content": msg.content,
        "created_at": msg.created_at.isoformat() if msg.created_at else None,
    }


def get_conversations():
    with SessionLocal() as session:
        conversations = session.query(Conversation).order_by(Conversation.created_at).all()
        return [serialize_conversation(conv) for conv in conversations]


def create_conversation(title: str):
    with SessionLocal() as session:
        conversation = Conversation(title=title)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return serialize_conversation(conversation)


def get_messages(conversation_id: int):
    with SessionLocal() as session:
        messages = (
            session.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
            .all()
        )
        return [serialize_message(msg) for msg in messages]


def create_message(conversation_id: int, role: str, content: str):
    with SessionLocal() as session:
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )
        session.add(message)
        session.commit()
        session.refresh(message)
        return serialize_message(message)


def delete_conversation(conversation_id: int):
    with SessionLocal() as session:
        conversation = session.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not conversation:
            return None
        session.query(Message).filter(Message.conversation_id == conversation_id).delete()
        session.delete(conversation)
        session.commit()
        return {"id": conversation_id}

