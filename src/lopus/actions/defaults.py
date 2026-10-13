"""Fábrica do conjunto inicial de ações do Lopus."""

from lopus.actions.filesystem import (
    InspectPathAction,
    ReadTextFileAction,
    WriteTextFileAction,
)
from lopus.actions.native_input import (
    CursorPositionAction,
    MoveCursorAction,
    NativeSystemInfoAction,
)
from lopus.actions.open_path import OpenPathAction
from lopus.actions.registry import ActionRegistry
from lopus.actions.shell import RunCommandAction
from lopus.native import NativeBridge


def create_default_action_registry() -> ActionRegistry:
    registry = ActionRegistry()
    native = NativeBridge()

    registry.register(InspectPathAction())
    registry.register(ReadTextFileAction())
    registry.register(WriteTextFileAction())
    registry.register(OpenPathAction())
    registry.register(RunCommandAction())

    registry.register(NativeSystemInfoAction(native))
    registry.register(CursorPositionAction(native))
    registry.register(MoveCursorAction(native))
    return registry
