from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from safety_detector import analyze_prompt
from hallucination_checker import check_grounding


BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"

app = FastAPI(
    title="SafeGuard AI",
    description="LLM safety, jailbreak detection and grounding prototype",
    version="1.0.0"
)

app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PromptRequest(BaseModel):
    prompt: str


class GroundingRequest(BaseModel):
    source: str
    response: str


@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/api/health")
def health():
    return {"status": "online", "service": "SafeGuard AI"}


@app.post("/api/analyze")
def analyze(request: PromptRequest):
    result = analyze_prompt(request.prompt)

    # Safe demo response. In a production system this would call an LLM
    # only after the security gate approves the prompt.
    if result["verdict"] == "BLOCK":
        demo_response = "Request blocked by SafeGuard AI security policy."
    elif result["verdict"] == "REVIEW":
        demo_response = "Request flagged for human review before LLM execution."
    else:
        demo_response = (
            "Demo response generated successfully. "
            "The prompt passed the prototype safety gate."
        )

    return {
        "security": result,
        "demo_response": demo_response,
        "pipeline": [
            "Input received",
            "Security scan completed",
            "Risk decision generated",
            "Response gate applied"
        ]
    }


@app.post("/api/grounding")
def grounding(request: GroundingRequest):
    return check_grounding(request.source, request.response)
