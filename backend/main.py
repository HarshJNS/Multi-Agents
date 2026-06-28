from __future__ import annotations

from pathlib import Path
from typing import Any
from uuid import uuid4

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from multi_agent_studio.core.orchestrator import MultiAgentOrchestrator

load_dotenv()


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    session_id: str | None = None


class AgentInfo(BaseModel):
    key: str
    name: str
    role: str
    description: str


app = FastAPI(
    title="Multi-Agent Studio API",
    version="1.0.0",
    description="Full-stack multi-agent AI engineering assistant backend.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = MultiAgentOrchestrator()
FRONTEND_DIST = Path(__file__).resolve().parents[1] / "frontend" / "dist"


@app.get("/api/health")
def health() -> dict[str, str | bool]:
    return {
        "status": "ready",
        "service": "multi-agent-studio",
        "provider": orchestrator.llm.provider_name,
        "model": orchestrator.llm.model,
        "live_model": orchestrator.llm.is_configured,
    }


@app.get("/api/agents")
def agents() -> dict[str, list[dict[str, str]]]:
    return {
        "agents": [
            {
                "key": "router",
                "name": "Router Agent",
                "role": "Traffic controller",
                "description": "Classifies the request and selects the right specialist.",
            },
            {
                "key": "ai_engineer",
                "name": "AI Engineer Agent",
                "role": "AI systems mentor",
                "description": "Handles AI architecture, learning paths, and implementation strategy.",
            },
            {
                "key": "research",
                "name": "Research Agent",
                "role": "Factual synthesis",
                "description": "Answers factual questions concisely and flags when live sources are needed.",
            },
            {
                "key": "code",
                "name": "Code Agent",
                "role": "Debugging and implementation",
                "description": "Reviews code, debugging plans, and engineering tradeoffs.",
            },
            {
                "key": "product",
                "name": "Product Strategy Agent",
                "role": "Roadmaps and positioning",
                "description": "Turns ideas into practical product plans and project roadmaps.",
            },
            {
                "key": "prompt_eval",
                "name": "Prompt & Evaluation Agent",
                "role": "Prompt and RAG quality",
                "description": "Improves prompts and designs evaluation checks for LLM workflows.",
            },
            {
                "key": "synthesizer",
                "name": "Synthesizer Agent",
                "role": "Final response editor",
                "description": "Converts specialist output into a clean final answer.",
            },
        ]
    }


@app.post("/api/chat")
def chat(request: ChatRequest) -> dict[str, Any]:
    message = request.message.strip()
    if not message:
        raise HTTPException(status_code=422, detail="Message cannot be empty.")

    result = orchestrator.run(message)
    session_id = request.session_id or str(uuid4())

    return {
        "session_id": session_id,
        "answer": result.final_answer,
        "routing": {
            "agent_key": result.routing.agent_key,
            "agent_name": result.routing.agent_name,
            "confidence": result.routing.confidence,
            "matched_signals": result.routing.matched_signals,
            "reason": result.routing.reason,
        },
        "primary": {
            "agent_key": result.primary.agent_key,
            "agent_name": result.primary.agent_name,
            "role": result.primary.role,
            "content": result.primary.content,
            "bullets": result.primary.bullets,
            "source": result.primary.source,
            "model": result.primary.model,
        },
        "trace": [
            {
                "agent_key": output.agent_key,
                "agent_name": output.agent_name,
                "role": output.role,
                "content": output.content,
                "bullets": output.bullets,
            }
            for output in result.agent_trace
        ],
    }


if FRONTEND_DIST.exists():
    assets_dir = FRONTEND_DIST / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{path:path}", include_in_schema=False)
    def serve_frontend(path: str) -> FileResponse:
        requested = FRONTEND_DIST / path
        if requested.is_file():
            return FileResponse(requested)
        return FileResponse(FRONTEND_DIST / "index.html")
