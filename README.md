# Agente de consultas con IA (Streamlit)

Agente conversacional que usa un LLM vía [Groq](https://groq.com/) con *function calling*. El modelo decide cuándo llamar a una herramienta y responde en español con base en los datos obtenidos. La interfaz web está hecha con Streamlit e incluye memoria de la conversación.

## Herramientas

| Herramienta | Qué hace |
|---|---|
| `consultar_tipo_cambio` | Tipo de cambio de una moneda (p. ej. USD) respecto al quetzal |
| `consultar_clima` | Clima actual de una ciudad |
| `consultar_noticias` | Noticias recientes sobre un tema o palabra clave |
| `consultar_definicion` | Definición de una palabra en inglés |
| `consultar_pais` | Información general de un país: capital, población, región, moneda e idiomas |
| `consultar_feriados` | Días feriados públicos de un país en un año dado |

## Instalación y ejecución local

Requiere Python 3.10 o superior.

```bash
python -m venv env
# Windows
env\Scripts\activate
# macOS / Linux
source env/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

## Configuración de la clave

**Local:** copia `.env.example` como `.env` y escribe tus claves:

```
GROQ_API_KEY=tu_clave_aquí
NEWSDATA_API_KEY=tu_clave_aquí
```

`NEWSDATA_API_KEY` solo hace falta para la herramienta de noticias. El archivo `.env` está en `.gitignore` y nunca se sube al repositorio.

**Streamlit Community Cloud:** en *Settings → Secrets* de la app, agrega:

```toml
GROQ_API_KEY = "tu_clave_aquí"
NEWSDATA_API_KEY = "tu_clave_aquí"
```

El agente busca `GROQ_API_KEY` primero en las variables de entorno y, si no la encuentra, en `st.secrets`.
