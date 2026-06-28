from multi_agent_studio.core.router import Router


def test_routes_code_requests_to_code_agent():
    router = Router()

    decision = router.route("debug this Python function and explain the error")

    assert decision.agent_key == "code"
    assert decision.confidence >= 0.6
    assert "debug" in decision.matched_signals


def test_routes_roadmap_requests_to_product_agent():
    router = Router()

    decision = router.route("make a roadmap for my AI engineering portfolio project")

    assert decision.agent_key == "product"
    assert "roadmap" in decision.matched_signals


def test_defaults_general_ai_question_to_ai_engineer():
    router = Router()

    decision = router.route("how should I learn AI engineering")

    assert decision.agent_key == "ai_engineer"
    assert decision.confidence > 0
