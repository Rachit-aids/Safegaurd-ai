import re
from typing import Dict, List


STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were", "of", "to", "in",
    "and", "or", "for", "on", "with", "as", "by", "this", "that",
    "it", "from", "be", "at", "which", "what", "who", "how"
}


def keywords(text: str) -> List[str]:
    words = re.findall(r"[a-zA-Z0-9]+", (text or "").lower())
    return [w for w in words if len(w) > 2 and w not in STOPWORDS]


def check_grounding(source: str, response: str) -> Dict:
    source_words = set(keywords(source))
    response_words = keywords(response)

    if not response_words:
        return {
            "grounding_score": 0,
            "hallucination_risk": "HIGH",
            "matched_keywords": [],
            "unmatched_keywords": [],
            "explanation": "No meaningful response content was supplied."
        }

    matched = sorted({w for w in response_words if w in source_words})
    unmatched = sorted({w for w in response_words if w not in source_words})

    score = round((len(matched) / max(1, len(set(response_words)))) * 100)

    if score >= 75:
        risk = "LOW"
    elif score >= 45:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    return {
        "grounding_score": score,
        "hallucination_risk": risk,
        "matched_keywords": matched[:30],
        "unmatched_keywords": unmatched[:30],
        "explanation": (
            "The response has strong lexical overlap with the supplied context."
            if risk == "LOW"
            else "Some response content is not supported by the supplied context."
        )
    }
