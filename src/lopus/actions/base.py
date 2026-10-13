"""Contratos compartilhados pelas ações utilitárias do Lopus-AI."""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Mapping, Protocol


class Permission(StrEnum):
    FILE_READ = "file.read"
    FILE_WRITE = "file.write"
    FILE_OPEN = "file.open"
    SHELL_EXECUTE = "shell.execute"
    GUI_CONTROL = "gui.control"
    KEYBOARD_CONTROL = "keyboard.control"
    SCREEN_CAPTURE = "screen.capture"


class PermissionChecker(Protocol):
    def require(self, *permissions: Permission) -> None: ...


@dataclass(slots=True)
class ActionContext:
    permissions: PermissionChecker
    actor: str = "lopus"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ActionResult:
    success: bool
    action: str
    message: str
    data: Mapping[str, Any] = field(default_factory=dict)


class ActionError(RuntimeError):
    """Erro controlado durante a execução de uma ação."""


class Action(ABC):
    name: str
    description: str = ""
    required_permissions: frozenset[Permission] = frozenset()
    parameters_schema: Mapping[str, Any] = {
        "type": "object",
        "properties": {},
        "additionalProperties": False,
    }
    agent_exposed: bool = False

    @property
    def tool_name(self) -> str:
        """Nome seguro para APIs de function/tool calling."""
        return re.sub(r"[^a-zA-Z0-9_-]", "__", self.name)

    def tool_schema(self) -> dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.tool_name,
                "description": self.description,
                "parameters": dict(self.parameters_schema),
            },
        }

    def run(self, context: ActionContext, **kwargs: Any) -> ActionResult:
        context.permissions.require(*self.required_permissions)
        return self.execute(context, **kwargs)

    @abstractmethod
    def execute(self, context: ActionContext, **kwargs: Any) -> ActionResult:
        """Executa a ação depois das permissões básicas serem validadas."""
