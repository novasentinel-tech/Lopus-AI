"""Primeiro contrato funcional da feature de documentos."""

from __future__ import annotations

from lopus.actions import ActionContext, ActionRegistry, ActionResult

from .structure import DocumentStructure, inspect_structure


class DocumentFeature:
    def __init__(self, actions: ActionRegistry, context: ActionContext) -> None:
        self.actions = actions
        self.context = context

    def inspect(self, path: str) -> DocumentStructure:
        return inspect_structure(path)

    def open(self, path: str, *, method: str = "auto") -> ActionResult:
        return self.actions.execute(
            "file.open",
            self.context,
            path=path,
            method=method,
        )
