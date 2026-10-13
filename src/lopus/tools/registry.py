"""Registro mínimo de ferramentas do runtime.

Ainda não executa ferramentas. Serve como contrato inicial para as próximas etapas.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

Tool = Callable[..., Any]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, name: str, tool: Tool) -> None:
        normalized = name.strip().lower()
        if not normalized:
            raise ValueError("O nome da ferramenta não pode ser vazio")
        self._tools[normalized] = tool

    def get(self, name: str) -> Tool:
        try:
            return self._tools[name.strip().lower()]
        except KeyError as exc:
            raise KeyError(f"Ferramenta não registrada: {name}") from exc

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._tools))
