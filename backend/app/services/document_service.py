# import fitz
# import logging
# from google import genai
# from app.repositories import document_repository
# import os
# import time
# from dotenv import load_dotenv

# load_dotenv()

# gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
# logger = logging.getLogger(__name__)
# UPLOAD_DIR = "app/uploads"


# def get_embedding(text: str) -> list[float]:
#     result = gemini_client.models.embed_content(
#         model="gemini-embedding-001",
#         contents=text
#     )
#     return result.embeddings[0].values

# def score_text_overlap(query: str, text: str) -> int:
#     query_tokens = {token.strip(".,!?;:\"'()[]{}").lower() for token in query.split() if token}
#     text_tokens = {token.strip(".,!?;:\"'()[]{}").lower() for token in text.split() if token}
#     return len(query_tokens & text_tokens)


# def extract_text_from_pdf(file_path: str) -> str:
#     doc = fitz.open(file_path)
#     text = ""
#     for page in doc:
#         text += page.get_text()
#     doc.close()
#     return text


# def split_into_chunks(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> list[str]:
#     words = text.split()
#     chunks = []
#     start = 0
#     while start < len(words):
#         chunk = words[start : start + chunk_size]
#         chunks.append(" ".join(chunk))
#         if start + chunk_size >= len(words):
#             break
#         start += chunk_size - chunk_overlap
#     return chunks


# def process_pdf(conversation_id: int, filename: str, file_path: str) -> dict:
#     document_repository.delete_collection(conversation_id)
#     document_repository.delete_documents_by_conversation(conversation_id)
#     document = document_repository.create_document(conversation_id, filename)
#     text = extract_text_from_pdf(file_path)
#     chunks = split_into_chunks(text)
    
#     embeddings = []
#     embedding_failed = False
#     for chunk in chunks:
#         try:
#             embedding = get_embedding(chunk)
#         except Exception:
#             embedding = []
#             embedding_failed = True
#         embeddings.append(embedding)
#         time.sleep(0.7)
    
#     if embedding_failed:
#         logger.warning(
#             "Embedding model unavailable for conversation %s; saving chunks for keyword fallback retrieval.",
#             conversation_id,
#         )
#     document_repository.save_chunks(document["id"], conversation_id, chunks, embeddings)
#     return {
#         "document_id": document["id"],
#         "filename": filename,
#         "chunks_count": len(chunks)
#     }


# def get_relevant_chunks_text_match(conversation_id: int, query: str, max_chunks: int = 5) -> str:
#     chunk_texts = document_repository.get_chunks_by_conversation(conversation_id)
#     if not chunk_texts:
#         return ""

#     scored = [
#         (score_text_overlap(query, chunk), chunk)
#         for chunk in chunk_texts
#     ]
#     scored.sort(key=lambda pair: pair[0], reverse=True)
#     top_chunks = [chunk for score, chunk in scored if score > 0][:max_chunks]
#     if not top_chunks:
#         top_chunks = chunk_texts[:max_chunks]
#     return "\n\n".join(top_chunks)


# def get_relevant_chunks(conversation_id: int, query: str, max_chunks: int = 5) -> str:
#     try:
#         query_embedding = get_embedding(query)
#     except Exception:
#         logger.warning(
#             "Falling back to keyword retrieval for conversation %s because embeddings are unavailable.",
#             conversation_id,
#         )
#         return get_relevant_chunks_text_match(conversation_id, query, max_chunks)

#     if not query_embedding:
#         return get_relevant_chunks_text_match(conversation_id, query, max_chunks)

#     try:
#         chunks = document_repository.get_relevant_chunks(conversation_id, query_embedding, max_chunks)
#     except Exception as exc:
#         logger.warning(
#             "Chroma retrieval failed: %s. Falling back to keyword retrieval.",
#             exc,
#         )
#         return get_relevant_chunks_text_match(conversation_id, query, max_chunks)

#     if not chunks:
#         return get_relevant_chunks_text_match(conversation_id, query, max_chunks)
#     return "\n\n".join(chunks)


# def get_document(conversation_id: int) -> dict | None:
#     return document_repository.get_document_by_conversation(conversation_id)

#LANGCHAIN IMPLEMENTATION

import fitz
import logging
import os
import shutil
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from app.repositories import document_repository

dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
load_dotenv(dotenv_path)

logger = logging.getLogger(__name__)
UPLOAD_DIR = "app/uploads"
CHROMA_DIR = "./chroma_db"


def get_gemini_api_key() -> str | None:
    return os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")


def get_embeddings() -> GoogleGenerativeAIEmbeddings:
    api_key = get_gemini_api_key()
    if not api_key:
        raise RuntimeError(
            "Gemini API key required. Set GEMINI_API_KEY or GOOGLE_API_KEY in your environment or .env file."
        )
    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=api_key
    )


def extract_text_from_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text


def get_vectorstore(conversation_id: int) -> Chroma:
    return Chroma(
        persist_directory=f"{CHROMA_DIR}/conversation_{conversation_id}",
        embedding_function=get_embeddings(),
        collection_name=f"conversation_{conversation_id}"
    )


def process_pdf(conversation_id: int, filename: str, file_path: str) -> dict:
    document_repository.delete_collection(conversation_id)
    document_repository.delete_documents_by_conversation(conversation_id)

    persist_dir = f"{CHROMA_DIR}/conversation_{conversation_id}"
    if os.path.exists(persist_dir):
        shutil.rmtree(persist_dir)

    document = document_repository.create_document(conversation_id, filename)
    text = extract_text_from_pdf(file_path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " "]
    )
    chunks = splitter.split_text(text)

    Chroma.from_texts(
        texts=chunks,
        embedding=get_embeddings(),
        persist_directory=f"{CHROMA_DIR}/conversation_{conversation_id}",
        collection_name=f"conversation_{conversation_id}"
    )

    return {
        "document_id": document["id"],
        "filename": filename,
        "chunks_count": len(chunks)
    }


def get_relevant_chunks(conversation_id: int, query: str, max_chunks: int = 3) -> str:
    try:
        vectorstore = get_vectorstore(conversation_id)
        retriever = vectorstore.as_retriever(search_kwargs={"k": max_chunks})
        docs = retriever.invoke(query)
        if not docs:
            return ""
        return "\n\n".join(getattr(d, "page_content", "") for d in docs)[:2000]
    except Exception as exc:
        logger.warning("Retrieval failed: %s", exc)
        return ""


def get_document(conversation_id: int) -> dict | None:
    return document_repository.get_document_by_conversation(conversation_id)