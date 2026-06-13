from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage
from backend.mcp.tools import search_docs, get_roadmap, get_checklist
from backend.core.config import settings

llm = ChatGroq(
    api_key=settings.groq_api_key,
    model="llama-3.1-8b-instant",
    temperature=0.3
)

SYSTEM_PROMPT = """You are LandRight, a friendly AI copilot for international students arriving in the US.
You talk like a helpful older student who has been through it all — warm, casual, and honest.
Not like a government website. Not robotic. Like a real person who genuinely wants to help.

You have access to a knowledge base about everything international students need to know:
visas, banking, housing, SSN, taxes, OPT, CPT, health insurance, credit building, and more.

Rules:
- Always be specific and actionable. Don't give vague advice.
- If you don't know something, say so honestly and tell them to check with their DSO.
- Keep answers concise but complete. Use bullet points when listing steps.
- Never give legal advice. For visa questions always recommend they verify with their DSO.
- Add a follow-up question at the end to keep the conversation going.
"""

def ask(question: str, stage: str = None) -> str:
    context_parts = []

    search_results = search_docs(question)
    context_parts.append(f"KNOWLEDGE BASE RESULTS:\n{search_results}")

    if stage:
        roadmap = get_roadmap(stage)
        context_parts.append(f"STUDENT'S CURRENT STAGE ROADMAP:\n{roadmap}")

    context = "\n\n".join(context_parts)

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"""
Here is relevant information from our knowledge base:

{context}

Now answer this question from an international student:
{question}

Remember to be helpful, specific, and end with a follow-up question.
""")
    ]

    response = llm.invoke(messages)
    return response.content