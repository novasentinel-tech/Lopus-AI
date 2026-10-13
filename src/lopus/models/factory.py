"""Criação do provider configurado."""

from __future__ import annotations

from lopus.config import LopusConfig
from lopus.models.base import ModelProvider
from lopus.models.demo import DemoProvider
from lopus.models.ollama import OllamaProvider


def create_model(config: LopusConfig) -> ModelProvider:
    if config.provider == "demo":
        return DemoProvider()
    if config.provider == "ollama":
        return OllamaProvider(
            model=config.model,
            base_url=config.ollama_url,
            timeout=config.request_timeout,
        )
    raise ValueError(f"Provider desconhecido: {config.provider!r}")
