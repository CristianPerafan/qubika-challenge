import os
import shutil

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_chroma import Chroma

import chromadb

load_dotenv()

CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = os.getenv("CHROMA_PORT", 8000)

CHROMA_PATH = "chroma"
def save_to_chroma(chunks: list[Document],embedding_model):
    """
    Save chunks to the chroma database
    Args:
        chunks (list[Document]): list of chunks
        embedding_model: embedding model
    """
    if os.path.exists(CHROMA_PATH):
        try:
            shutil.rmtree(CHROMA_PATH)
        except Exception as e:
            print(f"Error al eliminar {CHROMA_PATH}: {e}")

    db = Chroma.from_documents(
        chunks,
        persist_directory=CHROMA_PATH,
        embedding=embedding_model
    )
    # Persist the database

    return db

def load_from_chroma(embedding_model):
    """
    Load the chroma database
    Returns:
        Chroma: Chroma database
    """
    chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)

    vector_db = Chroma(
        client=chroma_client,
        collection_name='news',
        embedding_function=embedding_model
    )


    return vector_db

def save_to_chroma_v2(chunks: list[Document],embedding_model):
    """
    Save chunks to the chroma database
    Args:
        chunks (list[Document]): list of chunks
        embedding_model: embedding model
    """
    chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)

    if "news" in [c.name for c in chroma_client.list_collections()]:
        chroma_client.delete_collection('news')

    vector_db = Chroma(
        client=chroma_client,
        collection_name='news',
        embedding_function=embedding_model
    )

    vector_db.add_documents(chunks)

    return vector_db

