from fastapi.testclient import TestClient

from multi_agent_studio.core.llm import NoLLMProvider
from backend.main import app
from backend import main


main.orchestrator.llm = NoLLMProvider()
client = TestClient(app)


def test_health_endpoint_reports_ready():
    response = client.get("/api/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert data["service"] == "multi-agent-studio"
    assert "provider" in data


def test_agents_endpoint_lists_specialists():
    response = client.get("/api/agents")

    assert response.status_code == 200
    data = response.json()
    names = [agent["name"] for agent in data["agents"]]
    assert "AI Engineer Agent" in names
    assert "Prompt & Evaluation Agent" in names
    assert len(data["agents"]) >= 5


def test_chat_endpoint_returns_agent_trace():
    response = client.post(
        "/api/chat",
        json={"message": "Make a roadmap for my AI engineering portfolio"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["routing"]["agent_key"] == "product"
    assert data["answer"]
    assert data["trace"][0]["agent_name"] == "Router Agent"
