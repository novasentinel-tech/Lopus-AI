"""Registro de ações utilitárias disponíveis ao runtime."""

from __future__ import annotations

from typing import Any

from lopus.actions.base import Action, ActionContext, ActionResult


class ActionRegistry:
    def __init__(self) -> None:
        self._actions: dict[str, Action] = {}

    def register(self, action: Action) -> None:
        normalized = action.name.strip().lower()
        if not normalized:
            raise ValueError("O nome da ação não pode ser vazio")
        if normalized in self._actions:
            raise ValueError(f"Ação já registrada: {normalized}")
        self._actions[normalized] = action

    def get(self, name: str) -> Action:
        normalized = name.strip().lower()
        try:
            return self._actions[normalized]
        except KeyError as exc:
            raise KeyError(f"Ação não registrada: {normalized}") from exc

    def execute(
        self,
        name: str,
        context: ActionContext,
        **kwargs: Any,
    ) -> ActionResult:
        return self.get(name).run(context, **kwargs)

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._actions))
