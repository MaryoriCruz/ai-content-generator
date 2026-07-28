🇬🇧 [English](README.md) · 🇪🇸 [Español](README.es.md)

![Banner](assets/banner.png)

<p align="center">
  <a href="https://tu-demo.streamlit.app">🌐 Live Demo</a> ·
  <a href="https://github.com/MaryoriCruz/ai-content-generator">📂 Repository</a>
</p>

<p align="center">
<i>From a single topic to publish-ready content for four platforms, grounded in real data.</i>
</p>

---

# The Problem

Creating content for multiple platforms—such as blogs, LinkedIn, X (Twitter), and Instagram—is repetitive, time-consuming, and difficult to keep consistent.

While Large Language Models can generate text quickly, their output often suffers from three common issues:

- Hallucinated or outdated information.
- Generic writing that ignores platform-specific formats.
- No automated quality control before content reaches the user.

This project explores how combining retrieval, prompt orchestration, and automatic evaluation can produce AI-generated content that is both trustworthy and ready to publish.

---

# The Solution

**AI Content Generator** is an end-to-end Generative AI application that transforms a single topic into platform-specific content grounded in real-world information.

Instead of relying solely on an LLM prompt, the application enriches generation through two specialized retrieval modes:

**Financial Mode**

Retrieves real-time market data and financial news using Alpha Vantage before generating investment-related content.

**Scientific Mode (RAG)**

Retrieves relevant research papers from arXiv using ChromaDB and semantic search, allowing the model to generate explanations grounded in actual scientific literature.

Before any response reaches the user, a second LLM evaluates its quality. If the generated content does not meet the minimum quality threshold, the system automatically regenerates it.

The application can also generate a relevant image for each piece of content using HuggingFace, with Unsplash acting as a fallback source when necessary.

---

# Technical Details

## How It Works

1. User selects topic, audience and target platform.
2. Optional retrieval fetches financial data or scientific papers.
3. LangChain orchestrates the generation workflow.
4. Groq-hosted LLaMA models generate platform-specific content.
5. A second LLM evaluates quality.
6. Low-scoring generations are automatically regenerated.
7. The final content is delivered together with an optional AI-generated image.

---

## AI Pipeline

The application follows a multi-stage LLM architecture instead of relying on a single prompt.

User Input

↓

Optional Retrieval

• Alpha Vantage (Financial)

• arXiv + ChromaDB (Scientific RAG)

↓

Prompt Orchestration (LangChain)

↓

LLaMA (Groq)

↓

LLM-as-Judge

↓

Conditional Retry

↓

Final Response

---

## Guardrails (LLM-as-Judge)

Rather than trusting the first generation blindly, a second language model evaluates every response before it reaches the user.

Evaluation criteria include:

- Relevance
- Coherence
- Platform formatting

Responses scoring below **5/10** are regenerated automatically once, improving consistency without requiring user intervention.

---

## Tech Stack

### LLMs

- Groq
- LLaMA 3.1
- LLaMA 3.3

### AI Framework

- LangChain

### Retrieval

- ChromaDB
- HuggingFace Embeddings
- arXiv API

### Data

- Alpha Vantage API

### Frontend

- Streamlit

### Images

- HuggingFace Inference API
- Unsplash API

### Observability

- LangSmith

### DevOps

- Docker
- Docker Compose
- uv

---

# Results

The application was successfully tested across all supported platforms and both retrieval modes.

A representative evaluation using Scientific RAG on the topic **Large Language Models** produced the following results:

| Check | Result |
|--------|--------|
| Quality Score | 8/10 |
| Relevant | ✅ |
| Coherent | ✅ |
| Platform Format | ✅ |
| Grounded Sources | Real arXiv papers |

The Financial Mode was also validated using real market data (AAPL), retrieving live financial information before generating platform-specific content together with an automatically generated financial disclaimer.

All requests are traced through LangSmith, enabling request-level observability including prompts, latency, token usage and model outputs.

---

# What This Project Demonstrates

This project demonstrates the ability to:

- Design multi-step LLM systems instead of relying on single prompts.
- Build Retrieval-Augmented Generation (RAG) pipelines using semantic search.
- Ground AI-generated content in real external data sources.
- Implement automated quality assurance through an LLM-as-Judge architecture.
- Build production-oriented AI applications with observability and containerized deployment.
- Deliver complete AI products, from orchestration and retrieval to user interface and deployment.

---

# Future Improvements

- Resolve the current LangSmith SDK compatibility issue affecting trace logging.
- Add generation history and export functionality.
- Expand RAG sources beyond arXiv.
- Track generation cost and token consumption.
- Implement CI/CD pipelines.
- Add authentication and user accounts.
- Deploy on cloud infrastructure.

---

# Disclaimer

The generated content is intended for educational and demonstration purposes.

While retrieval grounding and automated quality evaluation improve reliability, users should always verify critical or sensitive information before publication.

---

# Author

Maryori Cruz

Developed during the **Artificial Intelligence Bootcamp at Factoría F5** as the final project for the **Generative AI & LLM Applications** module.
