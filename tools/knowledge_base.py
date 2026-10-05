import json
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data" / "knowledge_base.json"

def search_knowledge_base(query: str) -> list[dict]:
    """
    Search knowledge base articles using simple keyword matching.
    """

    with open(DATA_PATH, "r", encoding="utf-8") as file:
        articles = json.load(file)

    query = query.lower()

    results = []

    for article in articles:
        score = 0
        for keyword in article["keywords"]:
            if keyword.lower() in query:
                score += 1
        if score > 0:
            results.append({
                **article,
                "score": score
            })
    results.sort(key=lambda item: item["score"], reverse=True)
    return results[:3]