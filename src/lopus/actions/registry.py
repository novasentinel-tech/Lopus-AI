"""Registro de ações utilitárias disponíveis ao runtime."""

from __future__ import annotations

from typing import Any

from lopus.actions.base import Action, ActionContext, ActionResult


class ActionRegistry:
    def __init__(self) -> None:
        self._actions: dict[str, Action] = {}
        self._tool_names: dict[str, str] = {}

    def register(self, action: Action) -> None:
        normalized = action.name.strip().lower()
        if not normalized:
            raise ValueError("O nome da ação não pode ser vazio")
        if normalized in self._actions:
            raise ValueError(f"Ação já registrada: {normalized}")
        if action.tool_name in self._tool_names:
            raise ValueError(f"Nome de tool duplicado: {action.tool_name}")
        self._actions[normalized] = action
        self._tool_names[action.tool_name] = normalized

    def get(self, name: str) -> Action:
        normalized = name.strip().lower()
        try:
            return self._actions[normalized]
        except KeyError as exc:
            raise KeyError(f"Ação não registrada: {normalized}") from exc

    def get_by_tool_name(self, tool_name: str) -> Action:
        try:
            action_name = self._tool_names[tool_name]
        except KeyError as exc:
            raise KeyError(f"Tool não registrada: {tool_name}") from exc
        action = self._actions[action_name]
        if not action.agent_exposed:
            raise PermissionError(f"A tool {tool_name} não está exposta ao agente.")
        return action

    def execute(
        self,
        name: str,
        context: ActionContext,
        **kwargs: Any,
    ) -> ActionResult:
        return self.get(name).run(context, **kwargs)

    def execute_tool(
        self,
        tool_name: str,
        context: ActionContext,
        **kwargs: Any,
    ) -> ActionResult:
        return self.get_by_tool_name(tool_name).run(context, **kwargs)

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._actions))

    def agent_tool_schemas(self) -> tuple[dict[str, Any], ...]:
        return tuple(
            action.tool_schema()
            for action in sorted(self._actions.values(), key=lambda item: item.name)
            if action.agent_exposed
        )
