import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv
from src.rag import retrieve_relevant_context

print("Versión de Gradio:", gr.__version__)

load_dotenv()
client = OpenAI()

# -----------------------------
# Historial global (solo chat real). Este historial es el que se envía al modelo GPT para mantener coherencia. Gradio no lo usa, sólo lo usa OpenAI.
# -----------------------------
history = [
    {"role": "system", "content": "Eres un asistente experto en energía."}
]

# -----------------------------
# Función principal del chat
# -----------------------------
def rag_response(message, chat_history, modo_rag):
    global history # Esta función deberá usar y modificar la variable history que está definida afuera.

    # Recuperación RAG
    context = retrieve_relevant_context(message, k=5)

    # Modo SOLO RAG sin contexto. chat_history es el historial visual para la interfaz de Gradio.
    if modo_rag == "Solo RAG" and context is None:
        bot_msg = "No se encontró información relevante en los documentos."
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": bot_msg})
        chat_history.append({"role": "user", "content": message})
        chat_history.append({"role": "assistant", "content": bot_msg})
        return chat_history
    
    # Else
    # Prompt para el modelo (NO se guarda en historial)
    full_prompt = (
        f"Pregunta del usuario:\n{message}\n\n"
        f"Contexto recuperado:\n{context}\n\n"
        "Responde de forma clara y precisa."
    )

    # Guardar mensaje del usuario en historial
    history.append({"role": "user", "content": message})

    # Llamada a OpenAI
    messages_to_send = [
        history[0],  # system
        *history[1:-1],  # todo lo anterior excepto el último user que vamos a reemplazar
        {"role": "user", "content": full_prompt}
    ]

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages_to_send
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
    with gr.Blocks() as demo:
        gr.Markdown("# 🔌 Chatbot RAG sobre Energía")

        modo_rag = gr.Radio(
            ["Híbrido (RAG + Modelo)", "Solo RAG"],
            value="Híbrido (RAG + Modelo)",
            label="Modo"
        )

        # Chatbot en Gradio 6.x ya no necesita `type`
        chatbot = gr.Chatbot(height=400)
        msg = gr.Textbox(label="Escribe tu pregunta:")
        clear = gr.Button("Limpiar chat")

        # Llamada a la función rag_response
        msg.submit(
            rag_response,
            inputs=[msg, chatbot, modo_rag],
            outputs=chatbot
        )

        # Función para limpiar historial
        def clear_all():
            global history
            history = [history[0]]  # reset solo el system
            return []

        clear.click(clear_all, None, chatbot)

    return demo


if __name__ == "__main__":
    demo = build_interface()
    demo.launch()