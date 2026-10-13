"""Ações reutilizáveis que features e agentes podem solicitar ao runtime."""

from lopus.actions.base import Action, ActionContext, ActionError, ActionResult, Permission
from lopus.actions.defaults import create_default_action_registry
from lopus.actions.native_input import (
    ClickAction,
    CursorPositionAction,
    MoveCursorAction,
    NativeSystemInfoAction,
    TypeTextAction,
)
from lopus.actions.permissions import PermissionDeniedError, PermissionStore
from lopus.actions.registry import ActionRegistry
from lopus.actions.vision import (
    CaptureScreenAction,
    ClickTextAction,
    FindTextOnScreenAction,
    ReadScreenAction,
)

__all__ = [
    "Action",
    "ActionContext",
    "ActionError",
    "ActionRegistry",
    "ActionResult",
    "CaptureScreenAction",
    "ClickAction",
    "ClickTextAction",
    "CursorPositionAction",
    "FindTextOnScreenAction",
    "MoveCursorAction",
    "NativeSystemInfoAction",
    "Permission",
    "PermissionDeniedError",
    "PermissionStore",
    "ReadScreenAction",
    "TypeTextAction",
    "create_default_action_registry",
]
