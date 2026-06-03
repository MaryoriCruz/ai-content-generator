from langchain_core.prompts import PromptTemplate

instagram_prompt = PromptTemplate(
    input_variables=["topic", "audience", "language", "company_context"],
    template="""
Eres un experto en contenido para Instagram.

{company_context}

Crea una caption para Instagram sobre: {topic}
Audiencia objetivo: {audience}
Idioma: {language}

La caption debe tener:
- Primera línea muy impactante para el hook
- Desarrollo del mensaje con emojis
- Call to action claro
- 20 hashtags relevantes al final separados por espacios
- Entre 150 y 300 palabras

Responde SOLO con la caption, sin explicaciones adicionales.
"""
)