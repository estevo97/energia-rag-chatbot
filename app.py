import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv
import os

# Importamos nuestras funciones RAG
from src.rag import search_similar_chunks
from src.rag import retrieve_relevant_context
from src.utils import clean_text

load_dotenv()
client = OpenAI()


# -----------------------------
# Función principal del chat
# -----------------------------
def rag_response(message, history, modo_rag):

    # 1. Recuperar contexto relevante
    context = retrieve_relevant_context(message, k=5)

    # 2. Si está en modo "Solo RAG" y no hay contexto → no respondemos
    if modo_rag == "Solo RAG" and "No hay contexto" in context:
        return history + [[message, "No se encontró información relevante en los documentos."]]

    # 3. Construimos el prompt
    system_prompt = (
        "Eres un asistente experto en energía. "
        "Si el usuario pregunta algo que esté en los documentos, debes usar ese contexto. "
        "Si NO hay contexto relevante:\n"
        "- En modo 'Solo RAG': responde 'No se encontró información en los documentos'.\n"
        "- En modo 'Híbrido (RAG + Modelo)': responde con tu conocimiento general."
    )

    user_prompt = (
        f"Pregunta del usuario:\n{message}\n\n"
        f"Contexto recuperado:\n{context}\n\n"
        "Responde de forma clara y profesional."
    )

    # 4. Llamamos al modelo
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    )

    answer = completion.choices[0].message.content

    # 5. Actualizamos el historial y devolvemos
    history = history + [[message, answer]]
    return history


# -----------------------------
# Interfaz Gradio
# -----------------------------
def build_interface():

    with gr.Blocks(theme="soft") as demo:
        gr.Markdown("# 🔌 Chatbot RAG sobre Energía\n### Basado en FAISS + GPT-4o-mini")

        modo_rag = gr.Radio(
            ["Híbrido (RAG + Modelo)", "Solo RAG"],
            value="Híbrido (RAG + Modelo)",
            label="Modo de respuesta"
        )

        chatbot = gr.Chatbot(height=400)

        msg = gr.Textbox(label="Escribe tu pregunta:")
        clear = gr.Button("Limpiar chat")

        msg.submit(rag_response, inputs=[msg, chatbot, modo_rag], outputs=chatbot)
        clear.click(lambda: [], None, chatbot)

    return demo


if __name__ == "__main__":
    demo = build_interface()
    demo.launch()