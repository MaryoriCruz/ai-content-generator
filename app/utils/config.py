from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
UNSPLASH_API_KEY = os.getenv("UNSPLASH_API_KEY")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "ai-content-generator")


AVAILABLE_MODELS = {
    "LLaMA 3.1 8B (rápido)": "llama-3.1-8b-instant",
    "LLaMA 3.3 70B (potente)": "llama-3.3-70b-versatile",
    "Mixtral 8x7B (potente)": "mixtral-8x7b-32768"
}

def setup_langsmith():
    if LANGSMITH_API_KEY:
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_API_KEY"] = LANGSMITH_API_KEY
        os.environ["LANGCHAIN_PROJECT"] = LANGSMITH_PROJECT
        os.environ["LANGCHAIN_ENDPOINT"] = "https://eu.api.smith.langchain.com"
        import logging
        logging.getLogger("langsmith").setLevel(logging.CRITICAL)
        print(f"✅ LangSmith activo · proyecto: {LANGSMITH_PROJECT}")
    else:
        print("⚠️ LangSmith no configurado")