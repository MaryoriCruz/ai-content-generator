from langchain_core.prompts import PromptTemplate

linkedin_prompt = PromptTemplate(
    input_variables=["topic", "audience", "language", "company_context"],
    template="""
Eres un experto en contenido profesional para LinkedIn.

{company_context}

Crea una publicación para LinkedIn sobre: {topic}
Audiencia objetivo: {audience}
Idioma: {language}

La publicación debe tener:
- Apertura con una pregunta o dato impactante
- Historia o contexto personal/profesional
- 3 puntos clave con aprendizajes
- Conclusión reflexiva
- Call to action para generar conversación
- Entre 5 y 10 hashtags profesionales al final
- Entre 200 y 400 palabras

Responde SOLO con la publicación, sin explicaciones adicionales.
"""
)