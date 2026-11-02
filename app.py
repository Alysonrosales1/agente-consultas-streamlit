#######################
# Agente Basico De IA #
# Interfaz web        #
#######################

# Ejecutar con: streamlit run app.py

import json

import streamlit as st

from agent_core import MEMORY_MAX_MESSAGES, create_client, now_guatemala, process_response
from basic_memory import BasicMemory


st.set_page_config(
    page_title="Asistente de Consultas",
    page_icon="🧭",
    layout="centered",
    initial_sidebar_state="expanded",
)

WELCOME_MESSAGE = (
    "¡Hola! 👋 Soy tu asistente de consultas. Puedo ayudarte con **tipo de cambio**, "
    "**clima**, **noticias**, **definiciones en inglés**, **países** y **feriados**.\n\n"
    "¿Qué tema te gustaría consultar? También puedes elegir uno en la barra lateral."
)

TOPICS = [
    ("💱", "Tipo de cambio", "Quiero consultar el tipo de cambio"),
    ("🌤️", "Clima", "Quiero consultar el clima"),
    ("📰", "Noticias", "Quiero consultar noticias"),
    ("📖", "Definiciones en inglés", "Quiero consultar la definición de una palabra en inglés"),
    ("🌎", "Países", "Quiero consultar información de un país"),
    ("🎉", "Feriados", "Quiero consultar los feriados de un país"),
]

CUSTOM_CSS = """
<style>
/* Ocultar elementos por defecto de Streamlit */
#MainMenu, footer, [data-testid="stAppDeployButton"] { visibility: hidden; display: none; }
header[data-testid="stHeader"] { background: transparent; }

.block-container { padding-top: 2.5rem; padding-bottom: 6rem; }

/* Encabezado */
.hero {
    text-align: center;
    padding: 1.75rem 1.25rem 1.5rem;
    margin-bottom: 1.5rem;
    border-radius: 1.25rem;
    background:
        radial-gradient(circle at 15% 0%, rgba(99, 102, 241, 0.22), transparent 55%),
        radial-gradient(circle at 85% 100%, rgba(20, 184, 166, 0.18), transparent 55%);
    border: 1px solid rgba(128, 128, 160, 0.20);
}
.hero-icon { font-size: 2.6rem; line-height: 1; margin-bottom: 0.4rem; }
.hero h1 {
    font-size: 2.1rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin: 0;
    padding: 0;
    background: linear-gradient(90deg, #6366F1, #14B8A6);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero p { margin: 0.45rem 0 0; opacity: 0.75; font-size: 1rem; }
.hero .chip {
    display: inline-block;
    margin-top: 0.85rem;
    padding: 0.2rem 0.75rem;
    border-radius: 999px;
    font-size: 0.78rem;
    background: rgba(99, 102, 241, 0.12);
    border: 1px solid rgba(99, 102, 241, 0.25);
}

/* Burbujas de chat */
[data-testid="stChatMessage"] {
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.85rem;
    border-radius: 1.1rem;
    border: 1px solid rgba(128, 128, 160, 0.18);
    background: rgba(128, 128, 160, 0.07);
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    margin-right: 10%;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    flex-direction: row-reverse;
    margin-right: 0;
    margin-left: 10%;
    background: rgba(99, 102, 241, 0.13);
    border-color: rgba(99, 102, 241, 0.28);
    border-bottom-right-radius: 0.3rem;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
    border-bottom-left-radius: 0.3rem;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"] {
    text-align: right;
}
[data-testid="stChatMessageContent"] p { line-height: 1.6; }

/* Expander de herramientas */
[data-testid="stChatMessage"] [data-testid="stExpander"] details {
    border-radius: 0.75rem;
    font-size: 0.85rem;
}
[data-testid="stChatMessage"] [data-testid="stExpander"] summary { padding: 0.35rem 0.75rem; }

/* Barra lateral */
[data-testid="stSidebar"] .stButton button {
    width: 100%;
    justify-content: flex-start;
    text-align: left;
    padding: 0.55rem 0.9rem;
    transition: transform 0.12s ease, border-color 0.12s ease;
}
[data-testid="stSidebar"] .stButton button:hover { transform: translateX(3px); }
.sidebar-title { font-weight: 700; font-size: 1.05rem; margin: 0.25rem 0 0.15rem; }
.sidebar-sub { font-size: 0.82rem; opacity: 0.7; margin-bottom: 0.75rem; }
.note {
    font-size: 0.82rem;
    line-height: 1.55;
    padding: 0.8rem 0.9rem;
    border-radius: 0.75rem;
    background: rgba(128, 128, 160, 0.08);
    border: 1px solid rgba(128, 128, 160, 0.18);
}
.note b { display: block; margin-bottom: 0.15rem; }
.note ul { margin: 0 0 0.5rem 1rem; padding: 0; }
.note ul:last-child { margin-bottom: 0; }
</style>
"""


@st.cache_resource(show_spinner=False)
def get_client():
    return create_client()


def init_state():
    if "history" not in st.session_state:
        st.session_state.history = [
            {"role": "assistant", "content": WELCOME_MESSAGE, "tools": []}
        ]
    if "memory" not in st.session_state:
        st.session_state.memory = BasicMemory(max_messages=MEMORY_MAX_MESSAGES)
    if "pending_prompt" not in st.session_state:
        st.session_state.pending_prompt = None


def reset_conversation():
    for key in ("history", "memory", "pending_prompt"):
        st.session_state.pop(key, None)


def queue_prompt(text: str):
    st.session_state.pending_prompt = text


def render_tools(tools: list[dict]):
    if not tools:
        return
    names = ", ".join(dict.fromkeys(t["nombre"] for t in tools))
    with st.expander(f"🔧 Herramienta usada: {names}"):
        for t in tools:
            args = json.dumps(t["argumentos"], ensure_ascii=False)
            st.markdown(f"**{t['nombre']}**")
            st.code(args, language="json")
            resultado = t["resultado"]
            if not isinstance(resultado, str):
                resultado = json.dumps(resultado, ensure_ascii=False)
            st.caption(f"Resultado: {resultado}")


def render_sidebar():
    with st.sidebar:
        st.markdown('<div class="sidebar-title">🗂️ Temas disponibles</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="sidebar-sub">Toca un tema para empezar una consulta.</div>',
            unsafe_allow_html=True,
        )
        for emoji, label, example in TOPICS:
            st.button(
                f"{emoji}  {label}",
                key=f"topic_{label}",
                on_click=queue_prompt,
                args=(example,),
                width="stretch",
            )

        st.divider()
        st.button(
            "🧹  Nueva conversación",
            on_click=reset_conversation,
            type="primary",
            width="stretch",
        )

        st.divider()
        st.markdown(
            """
<div class="note">
<b>✅ Puede</b>
<ul>
<li>Consultar datos reales con sus 6 herramientas.</li>
<li>Recordar los últimos mensajes de la conversación.</li>
</ul>
<b>🚫 No puede</b>
<ul>
<li>Responder temas fuera de la lista.</li>
<li>Dar asesoría financiera, médica o legal.</li>
<li>Definir palabras en español.</li>
</ul>
</div>
""",
            unsafe_allow_html=True,
        )


def render_header():
    fecha = now_guatemala().strftime("%d/%m/%Y")
    st.markdown(
        f"""
<div class="hero">
  <div class="hero-icon">🧭</div>
  <h1>Asistente de Consultas</h1>
  <p>Tipo de cambio, clima, noticias, países y más, en una sola conversación.</p>
  <span class="chip">📍 Guatemala · {fecha}</span>
</div>
""",
        unsafe_allow_html=True,
    )


def main():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    init_state()
    render_sidebar()
    render_header()

    try:
        client = get_client()
    except Exception:
        st.error(
            "No se encontró la clave de API de Groq. Agrega `GROQ_API_KEY` a tu archivo "
            "`.env` y reinicia la aplicación."
        )
        st.stop()

    for message in st.session_state.history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            render_tools(message.get("tools", []))

    prompt = st.chat_input("Escribe tu consulta…")
    if st.session_state.pending_prompt:
        prompt = st.session_state.pending_prompt
        st.session_state.pending_prompt = None

    if not prompt or not prompt.strip():
        return
    prompt = prompt.strip()

    st.session_state.history.append({"role": "user", "content": prompt, "tools": []})
    with st.chat_message("user"):
        st.markdown(prompt)

    memory = st.session_state.memory
    with st.chat_message("assistant"):
        with st.spinner("Pensando…"):
            answer, tools = process_response(client, memory.messages(), prompt)
        answer = answer or "No tengo una respuesta para eso. ¿Puedes intentarlo de otra forma?"
        st.markdown(answer)
        render_tools(tools)

    st.session_state.history.append({"role": "assistant", "content": answer, "tools": tools})

    # Actualizar la memoria
    memory.add("user", prompt)
    memory.add("assistant", answer)


main()
