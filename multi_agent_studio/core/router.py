from __future__ import annotations

import re
from dataclasses import dataclass

from multi_agent_studio.core.models import RoutingDecision


@dataclass(frozen=True)
class AgentProfile:
    key: str
    name: str
    signals: tuple[str, ...]
    description: str


class Router:
    """Keyword-weighted router for the local multi-agent demo."""

    def __init__(self) -> None:
        self._profiles = (
            AgentProfile(
                key="code",
                name="Code Agent",
                signals=(
                    "code",
                    "debug",
                    "bug",
                    "error",
                    "function",
                    "python",
                    "javascript",
                    "api",
                    "review",
                    "refactor",
                ),
                description="Code review, debugging, implementation, and architecture help.",
            ),
            AgentProfile(
                key="product",
                name="Product Strategy Agent",
                signals=(
                    "roadmap",
                    "feature",
                    "mvp",
                    "startup",
                    "portfolio",
                    "project",
                    "plan",
                    "launch",
                    "pitch",
                ),
                description="Project framing, roadmap, feature planning, and product strategy.",
            ),
            AgentProfile(
                key="prompt_eval",
                name="Prompt & Evaluation Agent",
                signals=(
                    "prompt",
                    "rag",
                    "evaluation",
                    "eval",
                    "benchmark",
                    "dataset",
                    "quality",
                    "hallucination",
                    "retrieval",
                ),
                description="Prompt improvement, RAG checks, and evaluation design.",
            ),
            AgentProfile(
                key="research",
                name="Research Agent",
                signals=(
                    "what is",
                    "who is",
                    "capital",
                    "latest",
                    "research",
                    "compare",
                    "explain",
                    "facts",
                ),
                description="Concise factual answers and research-style synthesis.",
            ),
            AgentProfile(
                key="ai_engineer",
                name="AI Engineer Agent",
                signals=(
                    "ai",
                    "llm",
                    "agent",
                    "model",
                    "embedding",
                    "fine tune",
                    "machine learning",
                    "learn",
                    "engineering",
                ),
                description="AI engineering guidance, system design, and learning paths.",
            ),
        )

    def route(self, message: str) -> RoutingDecision:
        normalized = self._normalize(message)
        scores: dict[str, list[str]] = {}

        for profile in self._profiles:
            matches = [signal for signal in profile.signals if signal in normalized]
            if matches:
                scores[profile.key] = matches

        if not scores:
            profile = self._profile("ai_engineer")
            return RoutingDecision(
                agent_key=profile.key,
                agent_name=profile.name,
                confidence=0.45,
                matched_signals=["general"],
                reason="No specialist signal dominated, so the AI Engineer Agent handles the general request.",
            )

        best_key, matched = max(
            scores.items(),
            key=lambda item: (len(item[1]), self._priority(item[0])),
        )
        profile = self._profile(best_key)
        confidence = min(0.95, 0.52 + (0.11 * len(matched)))

        return RoutingDecision(
            agent_key=profile.key,
            agent_name=profile.name,
            confidence=round(confidence, 2),
            matched_signals=matched,
            reason=f"Matched {', '.join(matched[:4])}, which fits {profile.description.lower()}",
        )

    def _profile(self, key: str) -> AgentProfile:
        for profile in self._profiles:
            if profile.key == key:
                return profile
        raise KeyError(key)

    @staticmethod
    def _normalize(message: str) -> str:
        return re.sub(r"\s+", " ", message.lower()).strip()

    @staticmethod
    def _priority(key: str) -> int:
        priority = {
            "prompt_eval": 5,
            "code": 4,
            "product": 3,
            "research": 2,
            "ai_engineer": 1,
        }
        return priority.get(key, 0)

