import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv
from src.rag import retrieve_relevant_context

load_dotenv()
client = OpenAI()

# -----------------------------
# Historial global (solo chat real)
# -----------------------------
history = [
    {"role": "system", "content": "Eres un asistente experto en energía."}
]

# -----------------------------
# Función principal del chat
# -----------------------------
def rag_response(message, chat_history, modo_rag):
    global history

    # Recuperación RAG
    context = retrieve_relevant_context(message, k=5)

    # Modo SOLO RAG sin contexto
    if modo_rag == "Solo RAG" and "No hay contexto" in context:
        bot_msg = "No se encontró información relevante en los documentos."
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": bot_msg})
        chat_history.append({"role": "user", "content": message})
        chat_history.append({"role": "assistant", "content": bot_msg})
        return chat_history

    # Prompt para el modelo (NO se guarda en historial)
    full_prompt = (
        f"Pregunta del usuario:\n{message}\n\n"
        f"Contexto recuperado:\n{context}\n\n"
        "Responde de forma clara y precisa."
    )

    # Guardar mensaje del usuario en historial
    history.append({"role": "user", "content": message})

    # Llamada a OpenAI
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            history[0],  # system
            {"role": "user", "content": full_prompt}
        ]
    )

    answer = completion.choices[0].message.content

    # Guardar en historial real
    history.append({"role": "assistant", "content": answer})

    # Mostrar en Gradio
    chat_history.append({"role": "user", "content": message})
    chat_history.append({"role": "assistant", "content": answer})
    return chat_history


# -----------------------------
# Interfaz Gradio
# -----------------------------
def build_interface():
    with gr.Blocks(theme="soft") as demo:
        gr.Markdown("# 🔌 Chatbot RAG sobre Energía")

        modo_rag = gr.Radio(
            ["Híbrido (RAG + Modelo)", "Solo RAG"],
            value="Híbrido (RAG + Modelo)",
            label="Modo"
        )

        chatbot = gr.Chatbot(height=400, type="messages")
        msg = gr.Textbox(label="Escribe tu pregunta:")
        clear = gr.Button("Limpiar chat")

        msg.submit(
            rag_response,
            inputs=[msg, chatbot, modo_rag],
            outputs=chatbot
        )

        def clear_all():
            global history
            history = [history[0]]  # reset al system only
            return []

        clear.click(clear_all, None, chatbot)

    return demo


if __name__ == "__main__":
    demo = build_interface()
    demo.launch()