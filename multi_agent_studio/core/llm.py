from __future__ import annotations

import json
import os
import ssl
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class LLMRequest:
    agent_name: str
    agent_role: str
    user_message: str
    system_prompt: str


class LLMProvider(Protocol):
    provider_name: str
    model: str
    is_configured: bool

    def generate(self, request: LLMRequest) -> str:
        ...


class NoLLMProvider:
    provider_name = "local"
    model = "offline-rules"
    is_configured = False

    def generate(self, request: LLMRequest) -> str:
        raise RuntimeError("No live LLM provider is configured.")


class GeminiProvider:
    provider_name = "gemini"

    def __init__(self, api_key: str | None = None, model: str | None = None, timeout: int = 20) -> None:
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.model = _normalize_model(model or os.getenv("GEMINI_MODEL", "gemini-2.5-flash"))
        self.timeout = timeout

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key)

    def generate(self, request: LLMRequest) -> str:
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured.")

        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model}:generateContent?key={self.api_key}"
        )
        payload = {
            "systemInstruction": {"parts": [{"text": request.system_prompt}]},
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": request.user_message}],
                }
            ],
            "generationConfig": {
                "temperature": 0.35,
                "topP": 0.9,
                "maxOutputTokens": 180,
            },
        }
        encoded = json.dumps(payload).encode("utf-8")
        http_request = urllib.request.Request(
            url,
            data=encoded,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            context = _ssl_context()
            with urllib.request.urlopen(http_request, timeout=self.timeout, context=context) as response:
                data = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Gemini request failed: {detail}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"Gemini request failed: {exc.reason}") from exc

        return compact_text(_extract_gemini_text(data), max_words=90)


def build_llm_provider() -> LLMProvider:
    provider = GeminiProvider()
    if provider.is_configured:
        return provider
    return NoLLMProvider()


def compact_text(text: str, max_words: int = 90) -> str:
    cleaned = " ".join(text.strip().split())
    words = cleaned.split()
    if len(words) <= max_words:
        return cleaned
    return " ".join(words[:max_words]).rstrip(".,;:") + "..."


def _extract_gemini_text(data: dict) -> str:
    candidates = data.get("candidates") or []
    for candidate in candidates:
        content = candidate.get("content") or {}
        parts = content.get("parts") or []
        text = " ".join(part.get("text", "") for part in parts if part.get("text"))
        if text.strip():
            return text.strip()
    return "No concise answer was returned by Gemini."


def _ssl_context() -> ssl.SSLContext:
    try:
        import certifi

        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return ssl.create_default_context()


def _normalize_model(model: str) -> str:
    return model.removeprefix("models/")
