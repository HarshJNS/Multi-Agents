from __future__ import annotations

from multi_agent_studio.agents.specialists import SynthesizerAgent, build_specialists
from multi_agent_studio.core.llm import LLMProvider, build_llm_provider
from multi_agent_studio.core.models import AgentOutput, OrchestratorResult
from multi_agent_studio.core.router import Router


class MultiAgentOrchestrator:
    def __init__(self, llm: LLMProvider | None = None) -> None:
        self.router = Router()
        self.specialists = build_specialists()
        self.synthesizer = SynthesizerAgent()
        self.llm = llm or build_llm_provider()

    def run(self, message: str) -> OrchestratorResult:
        routing = self.router.route(message)
        router_output = AgentOutput(
            agent_key="router",
            agent_name="Router Agent",
            role="Traffic controller",
            content=routing.reason,
            bullets=[
                f"Selected: {routing.agent_name}",
                f"Confidence: {routing.confidence:.0%}",
                f"Signals: {', '.join(routing.matched_signals)}",
            ],
        )

        specialist = self.specialists[routing.agent_key]
        primary = specialist.run(message, routing, self.llm)
        synthesis = self.synthesizer.run(message, routing, primary)

        return OrchestratorResult(
            routing=routing,
            primary=primary,
            final_answer=synthesis.content,
            agent_trace=[router_output, primary, self.synthesizer.trace_output()],
        )
