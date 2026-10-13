"""Integração mínima com a API local do Ollama."""

from __future__ import annotations

import json
from collections.abc import Sequence
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from lopus.core.types import Message
from lopus.models.base import ModelError, ModelProvider


class OllamaProvider(ModelProvider):
    name = "ollama"

    def __init__(self, *, model: str, base_url: str, timeout: float = 120.0) -> None:
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def generate(self, messages: Sequence[Message]) -> str:
        payload = {
            "model": self.model,
            "messages": [message.as_dict() for message in messages],
            "stream": False,
        }
        request = Request(
            f"{self.base_url}/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urlopen(request, timeout=self.timeout) as response:
                data = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise ModelError(f"Ollama respondeu HTTP {exc.code}: {detail}") from exc
        except URLError as exc:
            raise ModelError(
                "Não foi possível conectar ao Ollama. Verifique se ele está em execução em "
                f"{self.base_url}."
            ) from exc
        except (json.JSONDecodeError, TimeoutError) as exc:
            raise ModelError(f"Resposta inválida ou timeout do Ollama: {exc}") from exc

        try:
            content = data["message"]["content"]
        except (KeyError, TypeError) as exc:
            raise ModelError("O Ollama retornou uma resposta em formato inesperado.") from exc

        if not isinstance(content, str) or not content.strip():
            raise ModelError("O Ollama retornou uma resposta vazia.")
        return content.strip()
