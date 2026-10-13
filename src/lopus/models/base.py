"""Contrato comum para providers de modelos."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any, Mapping

from lopus.core.types import Message
from lopus.models.tools import ModelTurn


class ModelError(RuntimeError):
    """Falha ao comunicar com ou executar um modelo."""


class ModelProvider(ABC):
    name: str

    @abstractmethod
    def generate(self, messages: Sequence[Message]) -> str:
        """Gera uma resposta textual a partir da conversa atual."""
        raise NotImplementedError

    def generate_with_tools(
        self,
        messages: Sequence[Mapping[str, Any]],
        tools: Sequence[Mapping[str, Any]],
    ) -> ModelTurn:
        """Executa uma rodada com ferramentas.

        Providers sem tool calling continuam funcionando: o método converte a
        conversa básica para ``Message`` e devolve somente texto.
        """
        del tools
        basic_messages: list[Message] = []
        for message in messages:
            role = str(message.get("role", ""))
            if role not in {"system", "user", "assistant"}:
                continue
            basic_messages.append(Message(role=role, content=str(message.get("content", ""))))  # type: ignore[arg-type]
        content = self.generate(basic_messages)
        return ModelTurn(
            content=content,
            assistant_message={"role": "assistant", "content": content},
        )
