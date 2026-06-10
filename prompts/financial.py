from langchain_core.prompts import PromptTemplate

financial_prompt = PromptTemplate(
    input_variables=["topic", "platform", "audience", "language", "company_context", "news_context"],
    template="""
Eres un experto en comunicación financiera y mercados.

{company_context}

{news_context}

Basándote en las noticias anteriores, crea contenido para {platform} sobre: {topic}
Audiencia objetivo: {audience}
Idioma: {language}

El contenido debe:
- Estar basado en las noticias reales proporcionadas
- Ser riguroso pero accesible
- Incluir datos concretos de las noticias
- Adaptarse al formato de {platform}
- Incluir disclaimer: "Este contenido es informativo, no constituye asesoramiento financiero"

Responde SOLO con el contenido listo para publicar.
"""
)