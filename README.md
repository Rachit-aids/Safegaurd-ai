# SafeGuard AI

PS-07 — AI Safety, Hallucination Reduction & Jailbreak Defense Engine.

## GitHub Pages Demo

The root `index.html` is intentionally at repository root so GitHub Pages can render the UI directly.

The GitHub Pages version runs the prototype detection and grounding logic in the browser, so it does **not** require a Python server.

### GitHub Pages
Enable:
`Settings → Pages → Deploy from branch → main → / (root)`

Then open:
`https://YOUR-USERNAME.github.io/Safeguard-ai/`

## Full-stack version

The `backend/` directory contains the FastAPI implementation for local/full-stack deployment.

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

## Main Features

- Prompt injection detection
- Jailbreak detection
- System prompt extraction detection
- Data exfiltration detection
- Risk scoring
- ALLOW / REVIEW / BLOCK verdicts
- Grounding / hallucination-risk prototype
- Analytics dashboard

> This is a hackathon prototype. Its heuristic scores are not a certified security or factuality guarantee.
