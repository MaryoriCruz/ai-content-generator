from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from app.utils.config import GROQ_API_KEY, AVAILABLE_MODELS
from prompts.blog import blog_prompt
from prompts.twitter import twitter_prompt
from prompts.instagram import instagram_prompt
from prompts.linkedin import linkedin_prompt

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

def generate_content(
    topic: str,
    platform: str,
    audience: str,
    language: str,
    model_name: str,
    company_name: str = "",
    company_description: str = "",
    tone: str = ""
) -> str:
    if company_name:
        company_context = f"""Estás generando contenido para: {company_name}
Descripción: {company_description}
Tono de voz: {tone}
Asegúrate de que el contenido refleje la identidad de esta marca."""
    else:
        company_context = ""

    prompt = PLATFORM_PROMPTS.get(platform, blog_prompt)
    llm = get_llm(model_name)
    chain = prompt | llm | StrOutputParser()

    return chain.invoke({
        "topic": topic,
        "audience": audience,
        "language": language,
        "company_context": company_context
    })