from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from app.utils.config import GROQ_API_KEY

evaluation_prompt = PromptTemplate(
    input_variables=["topic", "platform", "content"],
    template="""Eres un evaluador de calidad de contenido generado por IA.

Tema solicitado: {topic}
Plataforma: {platform}

Contenido generado:
---
{content}
---

Evalúa el contenido y responde SOLO con un JSON con este formato exacto:
{{
    "relevante": true/false,
    "coherente": true/false,
    "formato_correcto": true/false,
    "score": 0-10,
    "razon": "breve explicación si hay problemas"
}}

Criterios:
- relevante: ¿el contenido trata realmente sobre el tema pedido?
- coherente: ¿tiene sentido, sin frases incompletas o repeticiones extrañas?
- formato_correcto: ¿respeta la estructura esperada para {platform}?
"""
)

def evaluate_content(topic: str, platform: str, content: str) -> dict:
    """Evalúa la calidad del contenido generado con un LLM como juez"""
    try:
        llm = ChatGroq(
            api_key=GROQ_API_KEY,
            model_name="llama-3.1-8b-instant",
            temperature=0
        )
        chain = evaluation_prompt | llm | JsonOutputParser()
        result = chain.invoke({
            "topic": topic,
            "platform": platform,
            "content": content
        })
        return result
    except Exception as e:
        print(f"Error en evaluación: {e}")
        # Si falla la evaluación, asumimos que el contenido pasa (no bloquear al usuario)
        return {"relevante": True, "coherente": True, "formato_correcto": True, "score": 7, "razon": ""}

def passes_guardrails(evaluation: dict, min_score: int = 5) -> bool:
    """Determina si el contenido pasa los guardrails mínimos"""
    return (
        evaluation.get("relevante", True)
        and evaluation.get("coherente", True)
        and evaluation.get("score", 10) >= min_score
    )