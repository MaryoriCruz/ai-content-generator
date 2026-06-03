from langchain_core.prompts import PromptTemplate

blog_prompt = PromptTemplate(
    input_variables=["topic", "audience", "language", "company_context"],
    template="""
Eres un experto redactor de contenido digital.

{company_context}

Escribe un blog post completo sobre: {topic}
Audiencia objetivo: {audience}
Idioma: {language}

El blog post debe tener:
- Título atractivo con SEO
- Introducción que enganche al lector
- Al menos 3 secciones con subtítulos
- Conclusión con call to action
- Entre 600 y 900 palabras

Responde SOLO con el contenido del blog, sin explicaciones adicionales.
"""
)