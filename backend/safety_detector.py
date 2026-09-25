import re
from typing import List, Dict


PATTERNS = {
    "Prompt Injection": [
        r"ignore\s+(all\s+)?previous\s+instructions",
        r"ignore\s+the\s+system\s+prompt",
        r"disregard\s+(all\s+)?previous\s+instructions",
        r"override\s+(the\s+)?system",
        r"forget\s+(all\s+)?previous\s+instructions",
    ],
    "System Prompt Extraction": [
        r"reveal\s+(your\s+)?system\s+prompt",
        r"show\s+(me\s+)?your\s+system\s+message",
        r"print\s+your\s+hidden\s+instructions",
        r"what\s+are\s+your\s+system\s+instructions",
    ],
    "Jailbreak": [
        r"developer\s+mode",
        r"dan\s+mode",
        r"do\s+anything\s+now",
        r"bypass\s+(your\s+)?safety",
        r"remove\s+(your\s+)?restrictions",
        r"without\s+any\s+restrictions",
    ],
    "Data Exfiltration": [
        r"reveal\s+(private|secret|confidential)\s+data",
        r"give\s+me\s+api\s+keys",
        r"show\s+credentials",
        r"expose\s+passwords",
        r"leak\s+the\s+database",
    ],
    "Instruction Override": [
        r"new\s+instructions\s*:",
        r"from\s+now\s+on\s+you\s+must",
        r"your\s+new\s+rule\s+is",
        r"follow\s+my\s+instructions\s+instead",
    ],
}


def analyze_prompt(prompt: str) -> Dict:
    prompt = (prompt or "").strip()
    lower = prompt.lower()

    findings: List[Dict] = []
    categories = set()

    for category, patterns in PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, lower):
                findings.append({
                    "category": category,
                    "pattern": pattern,
                    "severity": "high" if category in {
                        "Jailbreak", "System Prompt Extraction", "Data Exfiltration"
                    } else "medium"
                })
                categories.add(category)
                break

    # Additional heuristic signals
    if lower.count("ignore") >= 2:
        findings.append({
            "category": "Repeated Override Language",
            "pattern": "multiple override tokens",
            "severity": "medium"
        })
        categories.add("Repeated Override Language")

    if len(prompt) > 4000:
        findings.append({
            "category": "Long Prompt",
            "pattern": "prompt length > 4000 characters",
            "severity": "low"
        })
        categories.add("Long Prompt")

    score = min(
        100,
        len(categories) * 22
        + sum(15 if f["severity"] == "high" else 8 if f["severity"] == "medium" else 3
              for f in findings)
    )

    if score >= 70:
        verdict = "BLOCK"
    elif score >= 35:
        verdict = "REVIEW"
    else:
        verdict = "ALLOW"

    if verdict == "BLOCK":
        explanation = "The prompt contains strong indicators of jailbreak, instruction override, extraction, or data-exfiltration behavior."
    elif verdict == "REVIEW":
        explanation = "The prompt contains suspicious instruction patterns and should be reviewed before being passed to an LLM."
    else:
        explanation = "No strong jailbreak or prompt-injection indicators were detected by the prototype rules."

    return {
        "risk_score": score,
        "verdict": verdict,
        "categories": sorted(categories),
        "findings": findings,
        "explanation": explanation,
    }
