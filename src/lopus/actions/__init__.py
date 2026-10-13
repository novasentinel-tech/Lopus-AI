"""Ações reutilizáveis que features e agentes podem solicitar ao runtime."""

from lopus.actions.base import (
    Action,
    ActionContext,
    ActionError,
    ActionResult,
    Permission,
)
from lopus.actions.defaults import create_default_action_registry
from lopus.actions.permissions import PermissionDeniedError, PermissionStore
from lopus.actions.registry import ActionRegistry

__all__ = [
    "Action",
    "ActionContext",
    "ActionError",
    "ActionRegistry",
    "ActionResult",
    "Permission",
    "PermissionDeniedError",
    "PermissionStore",
    "create_default_action_registry",
]
