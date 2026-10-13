"""Integração local com a API HTTP do Ollama."""

from __future__ import annotations

import json
from collections.abc import Sequence
from typing import Any, Mapping
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from lopus.core.types import Message
from lopus.models.base import ModelError, ModelProvider
from lopus.models.tools import ModelTurn, ToolCall


class OllamaProvider(ModelProvider):
    name = "ollama"

    def __init__(self, *, model: str, base_url: str, timeout: float = 120.0) -> None:
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _request(self, payload: Mapping[str, Any]) -> Mapping[str, Any]:
        request = Request(
            f"{self.base_url}/api/chat",
            data=json.dumps(dict(payload)).encode("utf-8"),
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
        if not isinstance(data, dict):
            raise ModelError("O Ollama retornou uma resposta inesperada.")
        return data

    def generate(self, messages: Sequence[Message]) -> str:
        data = self._request(
            {
                "model": self.model,
                "messages": [message.as_dict() for message in messages],
                "stream": False,
            }
        )
        try:
            content = data["message"]["content"]
        except (KeyError, TypeError) as exc:
            raise ModelError("O Ollama retornou uma resposta em formato inesperado.") from exc
        if not isinstance(content, str) or not content.strip():
            raise ModelError("O Ollama retornou uma resposta vazia.")
        return content.strip()

    def generate_with_tools(
        self,
        messages: Sequence[Mapping[str, Any]],
        tools: Sequence[Mapping[str, Any]],
    ) -> ModelTurn:
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": [dict(message) for message in messages],
            "stream": False,
        }
        if tools:
            payload["tools"] = [dict(tool) for tool in tools]

        data = self._request(payload)
        raw_message = data.get("message")
        if not isinstance(raw_message, dict):
            raise ModelError("O Ollama não retornou uma mensagem válida.")

        content = raw_message.get("content", "")
        if content is None:
            content = ""
        if not isinstance(content, str):
            content = str(content)

        parsed_calls: list[ToolCall] = []
        raw_calls = raw_message.get("tool_calls", []) or []
        if not isinstance(raw_calls, list):
            raise ModelError("Ollama retornou tool_calls em formato inválido.")

        for raw_call in raw_calls:
            if not isinstance(raw_call, dict):
                continue
            function = raw_call.get("function")
            if not isinstance(function, dict):
                continue
            name = function.get("name")
            if not isinstance(name, str) or not name.strip():
                continue
            arguments = function.get("arguments", {})
            if isinstance(arguments, str):
                try:
                    arguments = json.loads(arguments)
                except json.JSONDecodeError:
                    arguments = {}
            if not isinstance(arguments, dict):
                arguments = {}
            parsed_calls.append(ToolCall(name=name.strip(), arguments=arguments))

        if not content.strip() and not parsed_calls:
            raise ModelError("O Ollama retornou uma rodada vazia, sem texto ou tool calls.")

        assistant_message = dict(raw_message)
        assistant_message["role"] = "assistant"
        assistant_message.setdefault("content", content)
        return ModelTurn(
            content=content.strip(),
            tool_calls=tuple(parsed_calls),
            assistant_message=assistant_message,
        )
