import torch
import arxiv
import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import warnings
import logging
warnings.filterwarnings("ignore")
logging.getLogger("transformers").setLevel(logging.ERROR)

CHROMA_PATH = "data/chroma_db"
AI_CATEGORIES = ["cs.AI", "cs.LG", "cs.CL", "cs.CV", "cs.NE"]

def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

def fetch_arxiv_papers(topic: str, max_results: int = 5) -> list[Document]:
    """Busca papers de IA/ML en arXiv"""
    query = f"{topic} AND (cat:cs.AI OR cat:cs.LG OR cat:cs.CL OR cat:cs.CV)"
    
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )
    client = arxiv.Client()
    documents = []
    for paper in client.results(search):
        content = f"""
TÍTULO: {paper.title}
AUTORES: {', '.join(str(a) for a in paper.authors[:3])}
FECHA: {paper.published.strftime('%Y-%m-%d')}
CATEGORÍAS: {', '.join(paper.categories)}
RESUMEN: {paper.summary}
URL: {paper.entry_id}
"""
        documents.append(Document(
            page_content=content,
            metadata={
                "title": paper.title,
                "url": paper.entry_id,
                "published": paper.published.strftime('%Y-%m-%d'),
                "categories": ', '.join(paper.categories[:3])
            }
        ))
    return documents

def build_vectorstore(documents: list[Document], topic: str) -> Chroma:
    """Indexa los papers en ChromaDB"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(documents)
    embeddings = get_embeddings()
    
    # Usar colección única por topic para evitar mezclar papers
    collection_name = f"arxiv_{topic[:20].replace(' ', '_').lower()}"
    
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH,
        collection_name=collection_name
    )
    return vectorstore

def get_relevant_context(topic: str, max_papers: int = 5) -> tuple[str, list[dict]]:
    """
    Pipeline RAG completo:
    1. Busca papers en arXiv (IA/ML)
    2. Indexa en ChromaDB
    3. Recupera contexto relevante
    """
    documents = fetch_arxiv_papers(topic, max_results=max_papers)
    
    if not documents:
        return "No se encontraron papers científicos sobre este tema en arXiv.", []
    
    vectorstore = build_vectorstore(documents, topic)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    relevant_docs = retriever.invoke(topic)
    
    context = "CONTEXTO CIENTÍFICO DE PAPERS RECIENTES EN arXiv (IA/ML):\n\n"
    for i, doc in enumerate(relevant_docs, 1):
        context += f"Paper {i}:\n{doc.page_content}\n\n"
    
    papers_info = [
        {
            "title": doc.metadata.get("title", ""),
            "url": doc.metadata.get("url", ""),
            "published": doc.metadata.get("published", ""),
            "categories": doc.metadata.get("categories", "")
        }
        for doc in documents[:3]
    ]
    
    return context, papers_info