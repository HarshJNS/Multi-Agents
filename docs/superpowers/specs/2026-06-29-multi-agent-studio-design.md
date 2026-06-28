# Multi-Agent Studio Design

## Goal

Build a polished, runnable full-stack multi-agent AI engineering assistant that looks like a professional product and shows real routing between specialist agents.

## Scope

The first version is a professional local full-stack project, not a production SaaS. It must work without API keys, expose clear agent routing, and be easy to extend later with LLM providers.

## Architecture

The app uses FastAPI for the backend, React/Vite for the frontend, and a small Python package for the agent system. A router inspects the user prompt and chooses a specialist agent. The selected agent returns a structured response, and a synthesizer turns it into a clean final answer. The UI shows the final answer, current route, and execution trace in a product-grade dashboard.

## Agents

- Router Agent: classifies each message and records matched signals.
- AI Engineer Agent: answers AI engineering learning and implementation questions.
- Research Agent: handles factual questions and concise research-style answers.
- Code Agent: helps with debugging, architecture, and code review.
- Product Agent: creates roadmaps, feature plans, and project framing.
- Prompt & Evaluation Agent: improves prompts, evaluation plans, and RAG quality checks.
- Synthesizer Agent: formats the final response and keeps tone professional.

## UI

The React interface uses a dark professional dashboard layout with a sidebar for agent status, sample prompts, conversation controls, a command center header, chat console, and execution trace panel. The active agent appears with confidence and matched routing context.

## Testing

Unit tests cover routing and orchestration behavior. Manual verification runs the Streamlit app locally.
