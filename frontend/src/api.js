const API_BASE = import.meta.env.VITE_API_BASE || (import.meta.env.DEV ? "http://localhost:8000" : "");

export async function fetchAgents() {
  const response = await fetch(`${API_BASE}/api/agents`);
  if (!response.ok) {
    throw new Error("Could not load agents");
  }
  return response.json();
}

export async function fetchHealth() {
  const response = await fetch(`${API_BASE}/api/health`);
  if (!response.ok) {
    throw new Error("Could not load backend health");
  }
  return response.json();
}

export async function sendMessage(message, sessionId) {
  const response = await fetch(`${API_BASE}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, session_id: sessionId }),
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || "The agent backend rejected the request");
  }

  return response.json();
}
