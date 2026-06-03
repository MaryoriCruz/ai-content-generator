import requests
import os
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
UNSPLASH_API_KEY = os.getenv("UNSPLASH_API_KEY")

HF_API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"

def generate_smart_query(topic: str, platform: str) -> str:
    """Usa el LLM para generar un query de búsqueda óptimo para Unsplash"""
    from langchain_groq import ChatGroq
    from langchain_core.prompts import PromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    from app.utils.config import GROQ_API_KEY

    prompt = PromptTemplate(
        input_variables=["topic", "platform"],
        template="""Generate a short 3-5 word English search query for Unsplash 
to find a relevant image for this content.
Topic: {topic}
Platform: {platform}
Return ONLY the search query, nothing else. No quotes, no explanation."""
    )
    llm = ChatGroq(api_key=GROQ_API_KEY, model_name="llama-3.1-8b-instant", temperature=0)
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"topic": topic, "platform": platform}).strip()

def generate_image_huggingface(prompt: str) -> Image.Image | None:
    """Intenta generar imagen con HuggingFace"""
    try:
        response = requests.post(
            HF_API_URL,
            headers={"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"},
            json={"inputs": prompt},
            timeout=30
        )
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
        return None
    except Exception:
        return None

def get_unsplash_image(query: str) -> str | None:
    """Busca imagen en Unsplash con query optimizado"""
    try:
        response = requests.get(
            "https://api.unsplash.com/search/photos",
            params={"query": query, "per_page": 1, "orientation": "landscape"},
            headers={"Authorization": f"Client-ID {UNSPLASH_API_KEY}"},
            timeout=10
        )
        if response.status_code == 200:
            results = response.json().get("results", [])
            if results:
                return results[0]["urls"]["regular"]
        return None
    except Exception:
        return None

def get_image(topic: str, platform: str):
    """
    Estrategia:
    1. Intenta HuggingFace (imagen generada, perfectamente relevante)
    2. Si falla, usa Unsplash con query inteligente generado por LLM
    Devuelve: (imagen_PIL, url_string, fuente_string)
    """
    # Intento 1: HuggingFace
    hf_prompt = f"{topic}, {platform} content, professional, high quality"
    hf_image = generate_image_huggingface(hf_prompt)
    if hf_image:
        return hf_image, None, "HuggingFace"

    # Intento 2: Unsplash con query inteligente
    smart_query = generate_smart_query(topic, platform)
    url = get_unsplash_image(smart_query)
    if url:
        return None, url, f"Unsplash · query: _{smart_query}_"

    return None, None, None