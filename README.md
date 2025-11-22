# 🔌 Chatbot RAG sobre Energía


[![Open in Hugging Face](https://img.shields.io/badge/Open%20in-Hugging%20Face-blue)](https://huggingface.co/spaces/estevoag/energia-rag-chatbot)

**¡Haz clic aquí para abrir la app en vivo!**



Un **chatbot interactivo** basado en RAG (*Retrieval-Augmented Generation*) y GPT-4o-mini para responder preguntas sobre energía en España, utilizando tus documentos como fuente de información.

---

## 🚀 Funcionalidades

* ✅ Responde preguntas usando documentos (RAG)
* ✅ Modo híbrido: combina documentos + conocimiento general del modelo
* ✅ Mantiene historial de conversación
* ✅ Interfaz web amigable con **Gradio**

---

## 💡 Modos de funcionamiento

| Modo         | Descripción                                                                              | Ejemplo                                                                                      |
| ------------ | ---------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| **Solo RAG** | Solo responde con info de documentos. Si no hay contexto: indica que no hay información. | "¿Qué es la energía fotovoltaica?" → Devuelve solo contenido de documentos                   |
| **Híbrido**  | Usa contexto si hay, si no responde con conocimiento general del modelo                  | "Háblame de energías renovables en España" → Puede combinar contexto + conocimientos propios |

---

## 🖼 Demo de la Interfaz

**Chat visual en Gradio:**

```
Usuario: Qué es la energía solar?
Bot: La energía solar es...
```

**Selector de modo RAG/Híbrido:**

![Selector modo](https://img.shields.io/badge/Modo-RAG%20|%20Híbrido-yellow)

---

## 📦 Tecnologías usadas

* Python 3.10+
* OpenAI GPT-4o-mini
* Gradio 6.0.0
* FAISS (búsqueda semántica)
* PyPDF2 (extracción de texto PDF)
* dotenv (gestión de variables de entorno)

---

## ⚡ Cómo usarlo

### Local

1. Clona el repo:

```bash
git clone https://github.com/TU_USUARIO/energia-RAG-chatbot.git
cd energia-RAG-chatbot
```

2. Instala dependencias:

```bash
pip install -r requirements.txt
```

3. Configura la API key de OpenAI:

```bash
export OPENAI_API_KEY="tu_api_key_aqui"  # Linux / Mac
setx OPENAI_API_KEY "tu_api_key_aqui"    # Windows
```

4. Lanza la app:

```bash
python app.py
```

### Online en Hugging Face

[![Abrir en Hugging Face](https://img.shields.io/badge/Open%20en-Hugging%20Face-blue)](https://huggingface.co/spaces/TU_USUARIO/NOMBRE_DEL_SPACE)

---

## 📝 Estructura del proyecto

```
energia-RAG-chatbot/
│
├─ src/
│  ├─ rag.py        # Funciones RAG y búsqueda semántica
│  ├─ utils.py      # Lectura, limpieza y split de PDFs
│  └─ chat.py       # Funciones de chat y manejo de historial
│
├─ app.py           # Interfaz Gradio
├─ ingest.py        # Scripts para cargar documentos
├─ requirements.txt
└─ README.md
```

---

## 📌 Notas importantes

* ❌ No subir `.env` con tu API key
* El **historial** es útil sobre todo en modo híbrido
* El **modo Solo RAG** solo usa documentos como fuente

---

Hecho con dedicación por **Estevo Arias GArcía**.
