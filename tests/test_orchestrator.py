from multi_agent_studio.core.llm import NoLLMProvider
from multi_agent_studio.core.orchestrator import MultiAgentOrchestrator


def test_orchestrator_returns_structured_agent_result():
    orchestrator = MultiAgentOrchestrator(llm=NoLLMProvider())

    result = orchestrator.run("review this prompt for a RAG chatbot")

    assert result.routing.agent_key == "prompt_eval"
    assert result.primary.agent_name == "Prompt & Evaluation Agent"
    assert result.final_answer
    assert result.agent_trace
    assert result.agent_trace[0].agent_name == "Router Agent"


def test_orchestrator_keeps_simple_factual_answers_concise():
    orchestrator = MultiAgentOrchestrator(llm=NoLLMProvider())

    result = orchestrator.run("what is the capital of japan?")

    assert result.routing.agent_key == "research"
    assert "Tokyo" in result.final_answer
    assert len(result.final_answer.split()) < 80
