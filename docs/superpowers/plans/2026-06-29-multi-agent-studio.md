# Multi-Agent Studio Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a polished full-stack multi-agent AI engineering assistant that works locally and shows real specialist routing.

**Architecture:** Keep UI, API, and agent logic separate. `backend/main.py` exposes FastAPI routes, `frontend/src` renders React, `multi_agent_studio/core` owns routing and orchestration, and `multi_agent_studio/agents` owns specialist behavior.

**Tech Stack:** Python, FastAPI, React, Vite, pytest, dataclasses.

---

### Task 1: Routing Tests

**Files:**
- Create: `tests/test_router.py`
- Create: `multi_agent_studio/core/router.py`

- [x] Write tests for code, roadmap, and default AI engineering routing.
- [x] Implement keyword-weighted routing with confidence and matched signals.
- [x] Run `pytest tests/test_router.py -v`.

### Task 2: Orchestrator Tests

**Files:**
- Create: `tests/test_orchestrator.py`
- Create: `multi_agent_studio/core/orchestrator.py`
- Create: `multi_agent_studio/agents/specialists.py`

- [x] Write tests for structured agent results and concise factual responses.
- [x] Implement specialist agents and final synthesizer.
- [x] Run `pytest tests/test_orchestrator.py -v`.

### Task 3: Full-Stack UI

**Files:**
- Create: `backend/main.py`
- Create: `frontend/src/main.jsx`
- Create: `frontend/src/styles.css`
- Create: `frontend/src/api.js`
- Create: `requirements.txt`
- Create: `README.md`

- [x] Build a polished dark React interface.
- [x] Add FastAPI endpoints for health, agents, and chat.
- [x] Add sample prompts, agent status, final answers, and execution trace output.
- [x] Run `python -m compileall backend multi_agent_studio tests`.
- [x] Run `npm run build` inside `frontend`.
- [x] Run `uvicorn backend.main:app --port 8000`.
- [x] Run `npm run dev` inside `frontend`.
