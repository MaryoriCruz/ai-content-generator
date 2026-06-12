FROM python:3.12-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY pyproject.toml uv.lock ./

# Instalar dependencias
RUN uv sync --frozen --no-dev

# Copiar el código
COPY . .

# Crear carpeta de datos
RUN mkdir -p data/chroma_db

# Establecer variable de entorno para la ruta de la base de datos
ENV PYTHONPATH=/app

# Puerto de Streamlit
EXPOSE 8501

# Comando de arranque
CMD ["uv", "run", "streamlit", "run", "app/main.py", "--server.address=0.0.0.0", "--server.port=8501"]