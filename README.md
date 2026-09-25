# SafeGuard AI

SafeGuard AI is a lightweight LLM safety wrapper prototype for detecting prompt injection/jailbreak attempts and estimating response grounding/hallucination risk.

## Hackathon Problem
PS-07: AI Safety, Hallucination Reduction & Jailbreak Defense Engine.

## Features
- Prompt injection and jailbreak detection
- Risk scoring with explanations
- Safe / suspicious / blocked classification
- Demo response generation
- Grounding and hallucination-risk checks
- Security analytics dashboard
- FastAPI backend + responsive frontend
- Optional LLM API integration can be added later

## Tech Stack
- Python
- FastAPI
- Uvicorn
- HTML/CSS/JavaScript
- Rule-based security engine
- REST API

## Run locally

```bash
cd backend
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

Install:
```bash
pip install -r requirements.txt
```

Start:
```bash
uvicorn main:app --reload
```

Open:
`http://127.0.0.1:8000`

## Project Structure

```text
safeguard-ai/
├── backend/
│   ├── main.py
│   ├── safety_detector.py
│   ├── hallucination_checker.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── tests/
│   └── test_detector.py
├── .gitignore
└── README.md
```

## Important
This is a hackathon prototype. Its scores are heuristic/demo signals, not a certified security or factuality guarantee.
