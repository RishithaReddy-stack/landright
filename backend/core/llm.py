from langchain_groq import ChatGroq
from backend.core.config import settings

def get_llm():
    return ChatGroq(
        api_key=settings.groq_api_key,
        model="llama3-8b-8192",
        temperature=0.3
    )