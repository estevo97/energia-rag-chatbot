# src/ingest.py
from dotenv import load_dotenv
import os
from openai import OpenAI
import faiss
import numpy as np
from utils import read_pdf, split_text

load_dotenv()  # carga las variables desde .env
os.environ["OPENAI_API_KEY"]  # ya disponible para OpenAI

# Configura tu cliente OpenAI (asegúrate de tener tu API KEY en .env)
client = OpenAI()

PDF_FOLDER = "data/pdfs"
VECTORSTORE_FOLDER = "vectorstore"
EMBEDDING_DIM = 1536  # dimensión típica de OpenAI embeddings (text-embedding-3-small)

def generate_embedding(text):
    """Genera un embedding usando OpenAI"""
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return np.array(response.data[0].embedding, dtype=np.float32)

def main():
    all_chunks = []
    for file_name in os.listdir(PDF_FOLDER):
        if file_name.endswith(".pdf"):
            pdf_path = os.path.join(PDF_FOLDER, file_name)
            text = read_pdf(pdf_path)
            chunks = split_text(text)
            all_chunks.extend(chunks)
    
    if not all_chunks:
        print("No se encontraron PDFs en data/pdfs")
        return
    
    # Generar embeddings para todos los chunks
    embeddings = np.array([generate_embedding(chunk) for chunk in all_chunks])

    # Guardar en FAISS
    index = faiss.IndexFlatL2(EMBEDDING_DIM)
    index.add(embeddings)
    
    os.makedirs(VECTORSTORE_FOLDER, exist_ok=True)
    faiss.write_index(index, os.path.join(VECTORSTORE_FOLDER, "faiss_index.idx"))
    print(f"Embeddings generados y guardados en {VECTORSTORE_FOLDER}/faiss_index.idx")

if __name__ == "__main__":
    main()