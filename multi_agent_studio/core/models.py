from dataclasses import dataclass, field


@dataclass(frozen=True)
class RoutingDecision:
    agent_key: str
    agent_name: str
    confidence: float
    matched_signals: list[str]
    reason: str


@dataclass(frozen=True)
class AgentOutput:
    agent_key: str
    agent_name: str
    role: str
    content: str
    bullets: list[str] = field(default_factory=list)
    source: str = "local"
    model: str = "offline-rules"


@dataclass(frozen=True)
class OrchestratorResult:
    routing: RoutingDecision
    primary: AgentOutput
    final_answer: str
    agent_trace: list[AgentOutput]
