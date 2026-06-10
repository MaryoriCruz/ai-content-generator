import requests
import os
from dotenv import load_dotenv

load_dotenv()

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

def get_financial_news(topic: str, limit: int = 5) -> list[dict]:
    """Obtiene noticias financieras relevantes de Alpha Vantage"""
    try:
        response = requests.get(
            "https://www.alphavantage.co/query",
            params={
                "function": "NEWS_SENTIMENT",
                "tickers": topic.upper(),
                "limit": limit,
                "apikey": ALPHA_VANTAGE_API_KEY
            },
            timeout=10
        )
        data = response.json()
        
        if "feed" not in data:
            return []
            
        news = []
        for item in data["feed"][:limit]:
            news.append({
                "title": item.get("title", ""),
                "summary": item.get("summary", ""),
                "source": item.get("source", ""),
                "url": item.get("url", ""),
                "published": item.get("time_published", "")[:8]
            })
        return news
        
    except Exception as e:
        print(f"Error obteniendo noticias: {e}")
        return []

def format_news_context(news: list[dict]) -> str:
    """Formatea las noticias como contexto para el LLM"""
    if not news:
        return "No se encontraron noticias recientes."
    
    context = "NOTICIAS FINANCIERAS RECIENTES:\n\n"
    for i, item in enumerate(news, 1):
        context += f"{i}. {item['title']}\n"
        context += f"   Fuente: {item['source']} | Fecha: {item['published']}\n"
        context += f"   Resumen: {item['summary'][:200]}...\n\n"
    return context