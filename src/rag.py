from openai import OpenAI
import numpy as np
import faiss
import os
from dotenv import load_dotenv
from src.utils import read_pdf, clean_text, split_text

load_dotenv()
client = OpenAI()

VECTORSTORE_FOLDER = "vectorstore"
EMBEDDING_DIM = 1536  # mismo que ingest.py


def load_faiss_index():
    """Carga el índice FAISS desde disco."""
    index_path = os.path.join(VECTORSTORE_FOLDER, "faiss_index.idx")
    
    if not os.path.exists(index_path):
        raise FileNotFoundError(f"No existe el archivo {index_path}. Ejecuta primero ingest.py.")
    
    index = faiss.read_index(index_path)
    return index


def embed_query(query: str) -> np.ndarray:
    """Genera embedding para la pregunta del usuario."""
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )
    return np.array(response.data[0].embedding, dtype=np.float32)


def search_similar_chunks(query: str, k: int = 5):
    """Devuelve los k chunks más similares a la query."""
    index = load_faiss_index()
    query_emb = embed_query(query)

    # FAISS requiere array 2D
    query_emb = np.expand_dims(query_emb, axis=0)

    distances, indices = index.search(query_emb, k)

    return distances[0], indices[0]


def load_chunks():
    """Carga todos los chunks generados en ingest."""
    chunks_path = "data/chunks/chunks.txt"

    if not os.path.exists(chunks_path):
        raise FileNotFoundError("No se encontraron los chunks. Ejecuta ingest.py primero.")

    with open(chunks_path, "r", encoding="utf-8") as f:
        chunks = f.read().split("\n---\n")

    return chunks


def retrieve_relevant_context(query: str, k: int = 5, min_relevance: float = 1.0):
    """
    Devuelve los k fragmentos más relevantes ya listos para enviar al modelo GPT.
    Si NO hay fragmentos suficientemente relevantes → devuelve None.
    """
    distances, indices = search_similar_chunks(query, k)
    chunks = load_chunks()

    retrieved = []

    for dist, idx in zip(distances, indices):
        # descartar fragmentos con baja similitud (distancia demasiado alta)
        if dist > min_relevance:
            continue
        
        if idx < len(chunks):
            retrieved.append(f"[Relevancia: {round(dist, 2)}]\n{chunks[idx]}")

    # Si no se encontró nada realmente relevante
    if len(retrieved) == 0:
        return None

    context = "\n\n".join(retrieved)

    # si el texto es demasiado corto, se considera sin contexto útil
    if len(context.strip()) < 40:
        return None

    return context