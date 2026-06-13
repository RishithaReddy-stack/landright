from backend.db.qdrant import search

def search_docs(query: str) -> str:
    results = search(query, limit=3)
    if not results:
        return "No relevant information found."
    response = ""
    for r in results:
        response += f"**{r['title']}**\n{r['content'].strip()}\n\n---\n\n"
    return response

def get_roadmap(stage: str) -> str:
    stage_map = {
        "pre_arrival": ["esim_before_landing", "housing_pre_arrival"],
        "day_0": ["campus_checkin"],
        "week_1": ["bank_account", "state_id", "health_insurance"],
        "month_1": ["credit_building"],
        "ongoing": ["ssn", "taxes", "opt_cpt"]
    }
    from backend.knowledge.content import KNOWLEDGE_BASE
    kb = {item["id"]: item for item in KNOWLEDGE_BASE}
    ids = stage_map.get(stage.lower(), [])
    if not ids:
        return f"Unknown stage: {stage}. Try: pre_arrival, day_0, week_1, month_1, ongoing"
    response = f"Here's your roadmap for **{stage.replace('_', ' ').title()}**:\n\n"
    for i, id in enumerate(ids, 1):
        item = kb.get(id)
        if item:
            response += f"{i}. {item['title']}\n"
    return response

def get_checklist(stage: str) -> str:
    from backend.knowledge.content import KNOWLEDGE_BASE
    items = [i for i in KNOWLEDGE_BASE if i["category"] == stage.lower()]
    if not items:
        return f"No checklist found for stage: {stage}"
    response = f"Checklist for **{stage.replace('_', ' ').title()}**:\n\n"
    for item in items:
        response += f"- [ ] {item['title']}\n"
    return response