from multi_agent_studio.core.llm import LLMRequest, compact_text
from multi_agent_studio.core.orchestrator import MultiAgentOrchestrator


class FakeLLM:
    provider_name = "gemini"
    model = "gemini-test"
    is_configured = True

    def generate(self, request: LLMRequest) -> str:
        assert "crisp" in request.system_prompt.lower()
        return "Use Gemini. Keep router first. Return two bullets only."


class WeakLLM:
    provider_name = "gemini"
    model = "gemini-test"
    is_configured = True

    def generate(self, request: LLMRequest) -> str:
        return "Your AI Engineer Intern roadmap"


def test_orchestrator_uses_configured_llm_provider():
    orchestrator = MultiAgentOrchestrator(llm=FakeLLM())

    result = orchestrator.run("Design a multi-agent architecture")

    assert result.final_answer == "Use Gemini. Keep router first. Return two bullets only."
    assert result.primary.source == "gemini"
    assert result.primary.model == "gemini-test"


def test_compact_text_limits_wordy_model_output():
    text = " ".join(f"word{i}" for i in range(120))

    compact = compact_text(text, max_words=20)

    assert len(compact.split()) <= 21
    assert compact.endswith("...")


def test_weak_llm_answer_falls_back_to_useful_specialist_response():
    orchestrator = MultiAgentOrchestrator(llm=WeakLLM())

    result = orchestrator.run("ai engineer intern roadmap")

    assert result.primary.source == "local"
    assert "Focus on proof of skill" in result.final_answer
    assert "Weeks 1-2" in result.final_answer
