from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
UNSPLASH_API_KEY = os.getenv("UNSPLASH_API_KEY")

AVAILABLE_MODELS = {
    "LLaMA 3.1 8B (rápido)": "llama-3.1-8b-instant",
    "LLaMA 3.3 70B (potente)": "llama-3.3-70b-versatile",
    "Mixtral 8x7B (potente)": "mixtral-8x7b-32768"
}