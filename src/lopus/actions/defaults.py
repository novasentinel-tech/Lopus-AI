"""Fábrica do conjunto inicial de ações do Lopus."""

from collections.abc import Iterable

from lopus.actions.filesystem import InspectPathAction, ReadTextFileAction, WriteTextFileAction
from lopus.actions.native_input import (
    ClickAction,
    CursorPositionAction,
    MoveCursorAction,
    NativeSystemInfoAction,
    TypeTextAction,
)
from lopus.actions.open_path import OpenPathAction
from lopus.actions.registry import ActionRegistry
from lopus.actions.shell import RunCommandAction
from lopus.actions.vision import (
    CaptureScreenAction,
    ClickTextAction,
    FindTextOnScreenAction,
    ReadScreenAction,
)
from lopus.native import NativeBridge
from lopus.vision import RapidOCREngine


def create_default_action_registry(
    *,
    enabled_features: Iterable[str] | None = None,
    enabled_plugins: Iterable[str] | None = None,
) -> ActionRegistry:
    """Cria o registry padrão respeitando features e plugins habilitados.

    ``None`` em features/plugins mantém as capacidades experimentais disponíveis,
    útil para CLI e testes. No painel são fornecidas listas explícitas, fazendo os
    switches realmente controlarem quais Actions podem chegar ao agente.
    """
    registry = ActionRegistry()
    native = NativeBridge()
    feature_set = None if enabled_features is None else {item.strip() for item in enabled_features}
    plugin_set = None if enabled_plugins is None else {item.strip() for item in enabled_plugins}

    def feature_enabled(feature_id: str) -> bool:
        return feature_set is None or feature_id in feature_set

    def plugin_enabled(plugin_id: str) -> bool:
        return plugin_set is None or plugin_id in plugin_set

    registry.register(InspectPathAction())
    registry.register(ReadTextFileAction())
    registry.register(WriteTextFileAction())
    registry.register(OpenPathAction())
    registry.register(RunCommandAction())  # deliberadamente não exposta ao agente
    registry.register(NativeSystemInfoAction(native))

    if plugin_enabled("mouse_pointer"):
        registry.register(CursorPositionAction(native))
        registry.register(MoveCursorAction(native))
        registry.register(ClickAction(native))

    if plugin_enabled("keyboard_input"):
        registry.register(TypeTextAction(native))

    if feature_enabled("screen_perception") and plugin_enabled("screen_capture"):
        ocr = RapidOCREngine()
        registry.register(CaptureScreenAction(native))
        registry.register(ReadScreenAction(native, ocr))
        registry.register(FindTextOnScreenAction(native, ocr))
        if plugin_enabled("mouse_pointer"):
            registry.register(ClickTextAction(native, ocr))

    return registry
