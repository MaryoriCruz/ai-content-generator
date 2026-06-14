# ✨ AI Content Generator

Sistema de generación automática de contenido para redes sociales y blogs, potenciado por LLMs (Groq), LangChain, RAG con arXiv, noticias financieras en tiempo real y guardrails de calidad.

Proyecto desarrollado como parte del Bootcamp de IA — Proyecto LLMs: Generador de Contenido.

---

## 🚀 Demo

La aplicación permite generar contenido listo para publicar (Blog, Twitter/X, Instagram, LinkedIn) a partir de un tema, audiencia objetivo, idioma y perfil de marca opcional.

---

## 🧠 Características

### 🟢 Nivel Esencial
- Generación de contenido con prompts especializados por plataforma (Blog, Twitter/X, Instagram, LinkedIn)
- Interfaz web interactiva con Streamlit
- Selección de audiencia, tema y plataforma

### 🟡 Nivel Medio
- Selección entre dos modelos LLM (LLaMA 3.1 8B y LLaMA 3.3 70B vía Groq)
- Perfil de empresa/persona personalizable (nombre, descripción, tono de voz)
- Generación de imágenes relevantes al contenido (HuggingFace + fallback Unsplash con query inteligente generado por LLM)

### 🟠 Nivel Avanzado
- Trazabilidad completa de peticiones con **LangSmith**
- Generación de contenido en 4 idiomas: Español, Inglés, Francés e Italiano
- Modo noticias financieras con datos en tiempo real (Alpha Vantage) para tickers bursátiles
- RAG científico con **arXiv + ChromaDB**: genera contenido divulgativo sobre IA/ML basado en papers reales

### 🔴 Nivel Experto
- **Dockerización completa** de la aplicación con `uv` y Docker Compose
- **Guardrails / evaluación de calidad**: un segundo LLM evalúa relevancia, coherencia y formato del contenido generado (LLM-as-judge), con reintento automático si no supera el umbral mínimo

---

## 🛠️ Stack tecnológico

| Categoría | Tecnología |
|---|---|
| LLMs | Groq (LLaMA 3.1 8B / LLaMA 3.3 70B) |
| Framework LLM | LangChain |
| Trazabilidad | LangSmith |
| Frontend | Streamlit |
| Imágenes | HuggingFace Inference API + Unsplash API |
| Noticias financieras | Alpha Vantage API |
| RAG | arXiv API + ChromaDB + HuggingFace Embeddings |
| Contenedores | Docker + Docker Compose |
| Gestión de paquetes | uv |

---

## 📁 Estructura del proyecto

```
ai-content-generator/
├── app/
│   ├── main.py                  # App principal de Streamlit
│   ├── chains/
│   │   └── content_chain.py     # Lógica de generación + guardrails
│   ├── rag/
│   │   └── arxiv_rag.py          # Pipeline RAG con arXiv y ChromaDB
│   └── utils/
│       ├── config.py             # Configuración y variables de entorno
│       ├── financial_news.py     # Integración Alpha Vantage
│       ├── guardrails.py         # Evaluación de calidad LLM-as-judge
│       └── image_generator.py    # Generación/búsqueda de imágenes
├── prompts/
│   ├── blog.py
│   ├── twitter.py
│   ├── instagram.py
│   ├── linkedin.py
│   ├── financial.py
│   └── scientific.py
├── data/                          # Vector store de ChromaDB (no versionado)
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── uv.lock
└── .env.example
```

---

## ⚙️ Instalación

### Requisitos previos

- Python 3.12 (`requires-python = ">=3.12,<3.14"`)
- [uv](https://docs.astral.sh/uv/) instalado
- Cuentas gratuitas en: [Groq](https://console.groq.com), [HuggingFace](https://huggingface.co), [Unsplash](https://unsplash.com/developers), [Alpha Vantage](https://www.alphavantage.co/support/#api-key), [LangSmith](https://smith.langchain.com)

### 1. Clonar el repositorio

```bash
git clone https://github.com/Bootcamp-IA-P6/ai-content-generator.git
cd ai-content-generator
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
```

Rellena el `.env` con tus claves:

```env
GROQ_API_KEY=
HUGGINGFACE_API_KEY=
UNSPLASH_API_KEY=
ALPHA_VANTAGE_API_KEY=

LANGSMITH_API_KEY=
LANGSMITH_PROJECT=ai-content-generator
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=
LANGCHAIN_PROJECT=ai-content-generator
LANGCHAIN_ENDPOINT=https://eu.api.smith.langchain.com
```

> ⚠️ Si tu cuenta de LangSmith está en la región europea, es **imprescindible** configurar `LANGCHAIN_ENDPOINT`.

### 3. Instalar dependencias con uv

```bash
uv sync
```

### 4. Ejecutar la aplicación

```bash
uv run streamlit run app/main.py
```

Abre [http://localhost:8501](http://localhost:8501) en tu navegador.

---

## 🐳 Ejecución con Docker

```bash
docker-compose up --build
```

La aplicación estará disponible en [http://localhost:8501](http://localhost:8501).

> Usa siempre `--build` tras modificar código o dependencias, para que Docker Compose reconstruya la imagen.

---

## 🖥️ Uso

1. Selecciona el **modelo LLM** y el **idioma** en la barra lateral.
2. (Opcional) Activa **generación de imágenes**.
3. (Opcional) Activa el **modo noticias financieras** e introduce un ticker bursátil (ej. `AAPL`, `TSLA`, `BTC`).
4. (Opcional) Activa el **modo científico RAG** e introduce un tema de IA/ML (ej. `transformers`, `diffusion models`).
5. (Opcional) Completa el **perfil de empresa/persona** para personalizar el tono.
6. Escribe el **tema**, selecciona la **plataforma** y define la **audiencia objetivo**.
7. Pulsa **🚀 Generar contenido**.
8. Revisa la **evaluación de calidad (guardrails)** y, si aplica, los **papers de arXiv** utilizados como fuente.

---

## 🛡️ Guardrails

Tras generar el contenido, un segundo LLM evalúa:

- **Relevancia**: ¿el contenido trata sobre el tema solicitado?
- **Coherencia**: ¿el texto tiene sentido?
- **Formato**: ¿respeta la estructura esperada para la plataforma?

Si el contenido obtiene un score menor a 5/10, el sistema **reintenta automáticamente** la generación una vez.

---

## 📊 Trazabilidad

Todas las peticiones quedan registradas en [LangSmith](https://smith.langchain.com), incluyendo inputs, outputs, tokens consumidos y latencia, accesibles desde el proyecto `ai-content-generator`.

---

## 👤 Autora

## 👤 Autora

Maryori Cruz — Bootcamp de Inteligencia Artificial, Factoría F5

- 🔗 [Artículo en Medium]([text](https://medium.com/@maryori.eguizabal/de-cero-a-un-generador-de-contenido-con-ia-en-2-semanas-mi-proyecto-solo-con-langchain-rag-y-groq-bde533e34991))
- 💼 [LinkedIn]([text](https://www.linkedin.com/in/maryori-cruz/))
- 🐙 [GitHub](https://github.com/Bootcamp-IA-P6/ai-content-generator)
---

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver [LICENSE](./LICENSE) para más detalles.