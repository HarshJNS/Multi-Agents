from __future__ import annotations

from multi_agent_studio.core.llm import LLMProvider, LLMRequest, compact_text
from multi_agent_studio.core.models import AgentOutput, RoutingDecision


class SpecialistAgent:
    key = "base"
    name = "Specialist Agent"
    role = "Specialist"

    style = "Answer like a sharp AI agent: crisp, useful, no Wikipedia tone."

    def run(self, message: str, routing: RoutingDecision, llm: LLMProvider | None = None) -> AgentOutput:
        raise NotImplementedError

    def live_answer(self, message: str, llm: LLMProvider | None) -> AgentOutput | None:
        if not llm or not llm.is_configured:
            return None
        prompt = (
            f"{self.style}\n"
            "Rules: max 90 words. Use at most 3 bullets. No title. No markdown heading. "
            "No long intro. Give the answer directly. If code is needed, keep it minimal."
        )
        try:
            answer = llm.generate(
                LLMRequest(
                    agent_name=self.name,
                    agent_role=self.role,
                    user_message=message,
                    system_prompt=prompt,
                )
            )
        except RuntimeError:
            return None
        clean_answer = compact_text(answer, max_words=90)
        if not is_useful_answer(clean_answer):
            return None
        return AgentOutput(
            self.key,
            self.name,
            self.role,
            clean_answer,
            [],
            source=llm.provider_name,
            model=llm.model,
        )


class AIEngineerAgent(SpecialistAgent):
    key = "ai_engineer"
    name = "AI Engineer Agent"
    role = "AI systems mentor"

    def run(self, message: str, routing: RoutingDecision, llm: LLMProvider | None = None) -> AgentOutput:
        live = self.live_answer(message, llm)
        if live:
            return live
        bullets = [
            "Start with one clear AI workflow, not a giant platform.",
            "Use measurable behavior: inputs, outputs, latency, cost, and failure cases.",
            "Add evaluation early so improvements are visible instead of vibe-based.",
        ]
        return AgentOutput(
            self.key,
            self.name,
            self.role,
            "For AI engineering, think in systems: data, retrieval or model calls, orchestration, evaluation, and UX. Build a narrow workflow first, then make it reliable.",
            bullets,
        )


class ResearchAgent(SpecialistAgent):
    key = "research"
    name = "Research Agent"
    role = "Factual synthesis"

    def run(self, message: str, routing: RoutingDecision, llm: LLMProvider | None = None) -> AgentOutput:
        live = self.live_answer(message, llm)
        if live:
            return live
        normalized = message.lower()
        if "capital" in normalized and "japan" in normalized:
            content = "Tokyo is the capital of Japan."
            bullets = ["Answer: Tokyo", "Keep simple factual questions concise.", "Use sources when browsing is connected."]
        else:
            content = "Here is the concise research-style answer based on the request. For live facts, connect a web search provider and attach source links."
            bullets = ["Identify the factual claim.", "Check recency if the fact can change.", "Return sources beside the final answer."]
        return AgentOutput(self.key, self.name, self.role, content, bullets)


class CodeAgent(SpecialistAgent):
    key = "code"
    name = "Code Agent"
    role = "Debugging and implementation"

    def run(self, message: str, routing: RoutingDecision, llm: LLMProvider | None = None) -> AgentOutput:
        live = self.live_answer(message, llm)
        if live:
            return live
        bullets = [
            "Reproduce the issue with a small failing test or example.",
            "Inspect the boundary where data changes shape.",
            "Patch the smallest responsible module and rerun verification.",
        ]
        return AgentOutput(
            self.key,
            self.name,
            self.role,
            "I would approach this like a code review: isolate the failure, verify it with a test, then make the smallest fix that keeps the design clean.",
            bullets,
        )


class ProductAgent(SpecialistAgent):
    key = "product"
    name = "Product Strategy Agent"
    role = "Roadmaps and positioning"

    def run(self, message: str, routing: RoutingDecision, llm: LLMProvider | None = None) -> AgentOutput:
        live = self.live_answer(message, llm)
        if live:
            return live
        if "intern" in message.lower() and "roadmap" in message.lower():
            bullets = [
                "Weeks 1-2: Python, APIs, Git, basic ML, and one clean mini project.",
                "Weeks 3-4: RAG, embeddings, vector DBs, prompt design, and eval basics.",
                "Weeks 5-6: Build one agent app, document it well, deploy it, then apply.",
            ]
            return AgentOutput(
                self.key,
                self.name,
                self.role,
                "Focus on proof of skill, not certificates.",
                bullets,
            )
        bullets = [
            "Week 1: build one polished core workflow with sample prompts.",
            "Week 2: add persistence, better routing, and evaluation examples.",
            "Week 3: add optional LLM provider integration and a portfolio README.",
        ]
        return AgentOutput(
            self.key,
            self.name,
            self.role,
            "For a portfolio-grade AI project, ship a focused demo first: clear niche, visible agent collaboration, and a UI that explains decisions without exposing messy internals.",
            bullets,
        )


class PromptEvaluationAgent(SpecialistAgent):
    key = "prompt_eval"
    name = "Prompt & Evaluation Agent"
    role = "Prompt and RAG quality"

    def run(self, message: str, routing: RoutingDecision, llm: LLMProvider | None = None) -> AgentOutput:
        live = self.live_answer(message, llm)
        if live:
            return live
        bullets = [
            "Define what a good answer must include and what it must avoid.",
            "Add a small eval set with expected qualities, not only exact answers.",
            "Track retrieval relevance, groundedness, and final answer usefulness.",
        ]
        return AgentOutput(
            self.key,
            self.name,
            self.role,
            "For prompts and RAG systems, improve the prompt and the measurement together. A better prompt without an eval can still hide regressions.",
            bullets,
        )


class SynthesizerAgent(SpecialistAgent):
    key = "synthesizer"
    name = "Synthesizer Agent"
    role = "Final response editor"

    def run(self, message: str, routing: RoutingDecision, primary: AgentOutput) -> AgentOutput:
        parts = [primary.content]
        if primary.bullets:
            parts.append("\n".join(f"- {item}" for item in primary.bullets))
        return AgentOutput(
            self.key,
            self.name,
            self.role,
            "\n\n".join(parts),
            ["Combined specialist output", "Formatted a user-facing final response"],
        )

    def trace_output(self) -> AgentOutput:
        return AgentOutput(
            self.key,
            self.name,
            self.role,
            "Prepared the final answer from the selected specialist output.",
            ["Combined specialist output", "Formatted a user-facing final response"],
        )


def build_specialists() -> dict[str, SpecialistAgent]:
    agents: list[SpecialistAgent] = [
        AIEngineerAgent(),
        ResearchAgent(),
        CodeAgent(),
        ProductAgent(),
        PromptEvaluationAgent(),
    ]
    return {agent.key: agent for agent in agents}


def is_useful_answer(answer: str) -> bool:
    words = answer.split()
    if len(words) < 8:
        return False
    if len(answer) < 45:
        return False
    title_signals = ("roadmap", "guide", "plan", "overview")
    if len(words) <= 10 and any(signal in answer.lower() for signal in title_signals):
        return False
    return True
