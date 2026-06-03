from langchain_core.prompts import PromptTemplate

twitter_prompt = PromptTemplate(
    input_variables=["topic", "audience", "language", "company_context"],
    template="""
Eres un experto en redes sociales especializado en Twitter/X.

{company_context}

Crea un hilo de Twitter sobre: {topic}
Audiencia objetivo: {audience}
Idioma: {language}

El hilo debe tener:
- Entre 5 y 8 tweets
- Cada tweet máximo 280 caracteres
- Emojis relevantes
- Hashtags al final del último tweet
- Numerado así: 1/ 2/ 3/...

Responde SOLO con el hilo, sin explicaciones adicionales.
"""
)