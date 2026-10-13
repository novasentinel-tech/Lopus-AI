"""Configuração básica do Lopus-AI."""

from __future__ import annotations

import os
from dataclasses import dataclass, replace


@dataclass(slots=True)
class LopusConfig:
    provider: str = "demo"
    model: str = "qwen3:4b"
    ollama_url: str = "http://127.0.0.1:11434"
    max_messages: int = 24
    request_timeout: float = 120.0

    @classmethod
    def from_env(cls) -> "LopusConfig":
        return cls(
            provider=os.getenv("LOPUS_PROVIDER", "demo").strip().lower(),
            model=os.getenv("LOPUS_MODEL", "qwen3:4b").strip(),
            ollama_url=os.getenv("LOPUS_OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/"),
            max_messages=max(2, int(os.getenv("LOPUS_MAX_MESSAGES", "24"))),
            request_timeout=max(1.0, float(os.getenv("LOPUS_REQUEST_TIMEOUT", "120"))),
        )

    def with_overrides(self, *, provider: str | None = None, model: str | None = None) -> "LopusConfig":
        return replace(
            self,
            provider=(provider or self.provider).strip().lower(),
            model=(model or self.model).strip(),
        )
