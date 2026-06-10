import streamlit as st
from app.chains.content_chain import generate_content, PLATFORM_PROMPTS
from app.utils.config import AVAILABLE_MODELS, setup_langsmith
from app.utils.image_generator import get_image

# Activar LangSmith al arrancar
@st.cache_resource
def init_langsmith():
    setup_langsmith()

init_langsmith()

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
    generate_img = st.toggle("🖼️ Generar imagen", value=False)
    financial_mode = st.toggle("📈 Modo noticias financieras", value=False)
    scientific_mode = st.toggle("🔬 Modo científico RAG (IA/ML)", value=False)

    if financial_mode:
        st.info("💡 Introduce un ticker bursátil\nEj: AAPL, TSLA, MSFT, BTC")
    if scientific_mode:
        st.info("💡 Introduce un tema de IA/ML\nEj: transformers, diffusion models")
    if financial_mode and scientific_mode:
        st.warning("⚠️ Activa solo un modo a la vez")
        scientific_mode = False

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
        height=120,
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
        st.warning("⚠️ Por favor introduce un tema")
    elif not audience:
        st.warning("⚠️ Por favor define la audiencia")
    else:
        with st.spinner(f"✨ Generando contenido para {platform}..."):
            result, papers = generate_content(
                topic=topic,
                platform=platform,
                audience=audience,
                language=language,
                model_name=model,
                company_name=company_name,
                company_description=company_description,
                tone=tone,
                financial_mode=financial_mode,
                scientific_mode=scientific_mode
            )

        if papers:
            with st.expander("📚 Papers de arXiv utilizados como fuente"):
                for paper in papers:
                    st.markdown(f"- [{paper['title']}]({paper['url']}) — {paper['published']} — `{paper['categories']}`")

        image_pil, image_url, image_source = None, None, None
        if generate_img:
            with st.spinner("🎨 Generando imagen..."):
                image_pil, image_url, image_source = get_image(topic, platform)

        st.success("¡Contenido generado! ✅")
        st.divider()

        if image_pil:
            st.image(image_pil, caption=f"🤖 Generada con IA · {topic}", width="stretch")
            st.divider()
        elif image_url:
            st.image(image_url, caption=f"📷 {image_source}", width="stretch")
            st.divider()
        elif generate_img:
            st.info("No se pudo obtener imagen para este tema")

        tab1, tab2 = st.tabs(["📄 Vista previa", "📋 Copiar texto"])
        with tab1:
            st.markdown(result)
        with tab2:
            st.code(result, language=None)