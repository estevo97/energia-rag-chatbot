# src/utils.py
import PyPDF2

def read_pdf(file_path):
    """Lee un PDF y devuelve todo el texto como string."""
    text = ""
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def clean_text(text: str) -> str:
    import re
    text = text.replace("\x07", "")          # elimina BEL
    text = re.sub(r"\s+", " ", text)        # reemplaza saltos de línea, tabs, múltiples espacios por un solo espacio
    return text.strip()

def split_text(text, chunk_size=500, overlap=50):
    """
    Divide texto en chunks de tamaño aproximado `chunk_size` palabras
    con un overlap de `overlap` palabras.
    """
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks