from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from app.utils.config import GROQ_API_KEY, AVAILABLE_MODELS
from app.utils.financial_news import get_financial_news, format_news_context
from app.rag.arxiv_rag import get_relevant_context
from app.prompts.blog import blog_prompt
from app.prompts.twitter import twitter_prompt
from app.prompts.instagram import instagram_prompt
from app.prompts.linkedin import linkedin_prompt
from app.prompts.financial import financial_prompt
from app.prompts.scientific import scientific_prompt
from app.utils.guardrails import evaluate_content, passes_guardrails

PLATFORM_PROMPTS = {
    "Blog": blog_prompt,
    "Twitter/X": twitter_prompt,
    "Instagram": instagram_prompt,
    "LinkedIn": linkedin_prompt
}

def get_llm(model_name: str):
    model_id = AVAILABLE_MODELS.get(model_name, "llama-3.1-8b-instant")
    return ChatGroq(
        api_key=GROQ_API_KEY,
        model_name=model_id,
        temperature=0.7
    )

def _generate_raw(
    topic: str,
    platform: str,
    audience: str,
    language: str,
    model_name: str,
    company_name: str = "",
    company_description: str = "",
    tone: str = "",
    financial_mode: bool = False,
    scientific_mode: bool = False
) -> tuple[str, list[dict], dict]:

    if company_name:
        company_context = f"""Estás generando contenido para: {company_name}
Descripción: {company_description}
Tono de voz: {tone}
Asegúrate de que el contenido refleje la identidad de esta marca."""
    else:
        company_context = ""

    llm = get_llm(model_name)

    if financial_mode:
        news = get_financial_news(topic)
        news_context = format_news_context(news)
        chain = financial_prompt | llm | StrOutputParser()
        result = chain.invoke({
            "topic": topic,
            "platform": platform,
            "audience": audience,
            "language": language,
            "company_context": company_context,
            "news_context": news_context
        })
        return result, []

    if scientific_mode:
        scientific_context, papers = get_relevant_context(topic)
        chain = scientific_prompt | llm | StrOutputParser()
        result = chain.invoke({
            "topic": topic,
            "platform": platform,
            "audience": audience,
            "language": language,
            "company_context": company_context,
            "scientific_context": scientific_context
        })
        return result, papers

    prompt = PLATFORM_PROMPTS.get(platform, blog_prompt)
    chain = prompt | llm | StrOutputParser()
    result = chain.invoke({
        "topic": topic,
        "audience": audience,
        "language": language,
        "company_context": company_context
    })
    return result, []

def generate_content(
    topic: str,
    platform: str,
    audience: str,
    language: str,
    model_name: str,
    company_name: str = "",
    company_description: str = "",
    tone: str = "",
    financial_mode: bool = False,
    scientific_mode: bool = False
) -> tuple[str, list[dict], dict]:
    """
    Genera contenido y lo evalúa con guardrails.
    Si no pasa, reintenta una vez.
    Devuelve: (contenido, papers, evaluación)
    """
    result, papers = _generate_raw(
        topic, platform, audience, language, model_name,
        company_name, company_description, tone,
        financial_mode, scientific_mode
    )
    evaluation = evaluate_content(topic, platform, result)
    if not passes_guardrails(evaluation):
        result, papers = _generate_raw(
            topic, platform, audience, language, model_name,
            company_name, company_description, tone,
            financial_mode, scientific_mode
        )
        evaluation = evaluate_content(topic, platform, result)
    return result, papers, evaluation