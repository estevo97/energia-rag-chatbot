from dotenv import load_dotenv
import os
from openai import OpenAI
from rag import retrieve_relevant_context
from utils import split_text

load_dotenv()
client = OpenAI()

def build_prompt(question, context):
    """Construye prompt simple con contexto del RAG."""
    return f"""
Eres un asistente que responde preguntas usando el contexto proporcionado.

Contexto relevante:
{context}

Pregunta del usuario:
{question}

Si la respuesta no está en el contexto, responde: "No está en los documentos."
"""

def ask_gpt(prompt):
    """Envía prompt al modelo y devuelve la respuesta."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un asistente experto en análisis de documentos."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def chat(question):
    """Flujo RAG simplificado: recuperar contexto + preguntar al modelo."""
    print("🔍 Recuperando contexto...")
    chunks = retrieve_relevant_context(question, k=4)

    print("🧠 Construyendo prompt...")
    context = "\n\n".join(chunks) if chunks else ""

    prompt = build_prompt(question, context)

    print("🤖 Preguntando al modelo...")
    return ask_gpt(prompt)

# ---------------------------
# MODO CHAT INTERACTIVO
# ---------------------------

if __name__ == "__main__":
    print("\n💬 Chat RAG iniciado. Escribe 'salir' para terminar.\n")

    while True:
        pregunta = input("Tú: ")

        if pregunta.lower().strip() in ("salir", "exit", "quit"):
            print("👋 Saliendo del chat. Hasta luego!")
            break

        respuesta = chat(pregunta)
        print("\nBot:", respuesta, "\n")