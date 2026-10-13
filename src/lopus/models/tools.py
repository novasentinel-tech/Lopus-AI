"""Tipos usados pelo protocolo de tool calling entre modelos e o runtime."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class ToolCall:
    """Solicitação estruturada de uma ferramenta feita pelo modelo."""

    name: str
    arguments: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ModelTurn:
    """Uma rodada do modelo, podendo conter texto e chamadas de ferramentas."""

    content: str
    tool_calls: tuple[ToolCall, ...] = ()
    assistant_message: Mapping[str, Any] = field(default_factory=dict)
