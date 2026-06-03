import streamlit as st
from app.chains.content_chain import generate_content, PLATFORM_PROMPTS
from app.utils.config import AVAILABLE_MODELS

st.set_page_config(
    page_title="AI Content Generator",
    page_icon="✨",
    layout="wide"
)

st.title("✨ AI Content Generator")
st.markdown("Genera contenido listo para publicar en cualquier plataforma")

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Configuración")
    model = st.selectbox("🤖 Modelo LLM", list(AVAILABLE_MODELS.keys()))
    language = st.selectbox("🌍 Idioma", ["Español", "English", "Français", "Italiano"])

    st.divider()
    st.subheader("🏢 Perfil (opcional)")
    company_name = st.text_input("Nombre empresa/persona")
    company_description = st.text_area("Descripción breve", height=80)
    tone = st.selectbox("Tono de voz", ["Profesional", "Cercano", "Técnico", "Inspirador", "Divertido"])

# --- Main ---
col1, col2 = st.columns(2)

with col1:
    topic = st.text_area(
        "📝 ¿Sobre qué quieres generar contenido?",
        height=100,
        placeholder="Ej: Los beneficios de la IA en la educación"
    )

with col2:
    platform = st.selectbox("📱 Plataforma", list(PLATFORM_PROMPTS.keys()))
    audience = st.text_input(
        "👥 Audiencia objetivo",
        placeholder="Ej: Profesionales de marketing, 25-40 años"
    )

# --- Generar ---
if st.button("🚀 Generar contenido", type="primary", use_container_width=True):
    if not topic:
        st.warning("Por favor introduce un tema")
    elif not audience:
        st.warning("Por favor define la audiencia")
    else:
        with st.spinner(f"Generando contenido para {platform}..."):
            result = generate_content(
                topic=topic,
                platform=platform,
                audience=audience,
                language=language,
                model_name=model,
                company_name=company_name,
                company_description=company_description,
                tone=tone
            )

        st.success("¡Contenido generado! ✅")
        st.divider()
        st.markdown(result)
        st.divider()
        st.code(result, language=None)