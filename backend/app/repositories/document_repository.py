# import json
# import logging
# import chromadb
# from app.models.document import Document
# from app.models.chunk import Chunk
# from app.database.db import SessionLocal

# logger = logging.getLogger(__name__)
# chroma_client = chromadb.PersistentClient(path="./chroma_db")


# def get_or_create_collection(conversation_id: int):
#     return chroma_client.get_or_create_collection(
#         name=f"conversation_{conversation_id}"
#     )


# def delete_collection(conversation_id: int):
#     collection_name = f"conversation_{conversation_id}"
#     try:
#         chroma_client.delete_collection(name=collection_name)
#     except Exception:
#         pass


# def delete_documents_by_conversation(conversation_id: int):
#     with SessionLocal() as session:
#         documents = session.query(Document).filter(Document.conversation_id == conversation_id).all()
#         for document in documents:
#             session.delete(document)
#         session.commit()


# def get_chunks_by_conversation(conversation_id: int) -> list[str]:
#     with SessionLocal() as session:
#         chunks = (
#             session.query(Chunk)
#             .join(Document, Document.id == Chunk.document_id)
#             .filter(Document.conversation_id == conversation_id)
#             .order_by(Chunk.chunk_index)
#             .all()
#         )
#         return [chunk.content for chunk in chunks]


# def create_document(conversation_id: int, filename: str) -> dict:
#     with SessionLocal() as session:
#         document = Document(conversation_id=conversation_id, filename=filename)
#         session.add(document)
#         session.commit()
#         session.refresh(document)
#         return {"id": document.id, "filename": document.filename}


# def save_chunks(document_id: int, conversation_id: int, chunks: list[str], embeddings: list[list[float]]):
#     if not chunks:
#         logger.warning(
#             "No chunks extracted for document %s in conversation %s. Skipping Chroma storage.",
#             document_id,
#             conversation_id,
#         )
#         return

#     valid_embeddings = (
#         len(embeddings) == len(chunks)
#         and len(embeddings) > 0
#         and all(isinstance(e, list) and len(e) for e in embeddings)
#     )

#     if valid_embeddings:
#         collection = get_or_create_collection(conversation_id)
#         try:
#             collection.add(
#                 documents=chunks,
#                 embeddings=embeddings,
#                 ids=[f"doc_{document_id}_chunk_{i}" for i in range(len(chunks))]
#             )
#         except Exception as exc:
#             logger.warning(
#                 "Failed to add document %s chunks to Chroma for conversation %s: %s",
#                 document_id,
#                 conversation_id,
#                 exc,
#             )
#     else:
#         logger.warning(
#             "Invalid or missing embeddings for document %s in conversation %s. Chroma storage skipped.",
#             document_id,
#             conversation_id,
#         )

#     with SessionLocal() as session:
#         for i, chunk_text in enumerate(chunks):
#             chunk_row = Chunk(
#                 document_id=document_id,
#                 content=chunk_text,
#                 chunk_index=i,
#             )
#             session.add(chunk_row)
#         session.commit()

# def get_document_by_conversation(conversation_id: int) -> dict | None:
#     with SessionLocal() as session:
#         document = (
#             session.query(Document)
#             .filter(Document.conversation_id == conversation_id)
#             .order_by(Document.created_at.desc())
#             .first()
#         )
#         if not document:
#             return None
#         return {"id": document.id, "filename": document.filename}


#Langchain integration
import chromadb
from app.models.document import Document
from app.database.db import SessionLocal

chroma_client = chromadb.PersistentClient(path="./chroma_db")


def delete_collection(conversation_id: int):
    try:
        chroma_client.delete_collection(name=f"conversation_{conversation_id}")
    except Exception:
        pass


def create_document(conversation_id: int, filename: str) -> dict:
    with SessionLocal() as session:
        document = Document(
            conversation_id=conversation_id,
            filename=filename
        )
        session.add(document)
        session.commit()
        session.refresh(document)
        return {"id": document.id, "filename": document.filename}


def delete_documents_by_conversation(conversation_id: int):
    with SessionLocal() as session:
        documents = (
            session.query(Document)
            .filter(Document.conversation_id == conversation_id)
            .all()
        )
        for document in documents:
            session.delete(document)
        session.commit()


def get_document_by_conversation(conversation_id: int) -> dict | None:
    with SessionLocal() as session:
        document = (
            session.query(Document)
            .filter(Document.conversation_id == conversation_id)
            .order_by(Document.created_at.desc())
            .first()
        )
        if not document:
            return None
        return {"id": document.id, "filename": document.filename}