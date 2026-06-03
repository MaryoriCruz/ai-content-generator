from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

AVAILABLE_MODELS = {
    "LLaMA 3 8B (rápido)": "llama3-8b-8192",
    "Mixtral 8x7B (potente)": "mixtral-8x7b-32768"
}