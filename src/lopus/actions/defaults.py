"""Fábrica do conjunto inicial de ações do Lopus."""

from lopus.actions.filesystem import (
    InspectPathAction,
    ReadTextFileAction,
    WriteTextFileAction,
)
from lopus.actions.open_path import OpenPathAction
from lopus.actions.registry import ActionRegistry
from lopus.actions.shell import RunCommandAction


def create_default_action_registry() -> ActionRegistry:
    registry = ActionRegistry()
    registry.register(InspectPathAction())
    registry.register(ReadTextFileAction())
    registry.register(WriteTextFileAction())
    registry.register(OpenPathAction())
    registry.register(RunCommandAction())
    return registry
