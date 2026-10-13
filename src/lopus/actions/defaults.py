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
from lopus.actions.vision import CaptureScreenAction, FindTextOnScreenAction, ReadScreenAction
from lopus.native import NativeBridge
from lopus.vision import RapidOCREngine


def create_default_action_registry(
    *,
    enabled_features: Iterable[str] | None = None,
) -> ActionRegistry:
    """Cria o registry padrão.

    ``enabled_features=None`` mantém todas as features experimentais disponíveis,
    útil para CLI/testes. Quando uma coleção é informada (painel), apenas as
    Actions condicionais das features habilitadas são registradas.
    """
    registry = ActionRegistry()
    native = NativeBridge()
    feature_set = None if enabled_features is None else {item.strip() for item in enabled_features}

    registry.register(InspectPathAction())
    registry.register(ReadTextFileAction())
    registry.register(WriteTextFileAction())
    registry.register(OpenPathAction())
    registry.register(RunCommandAction())  # deliberadamente não exposta ao agente

    registry.register(NativeSystemInfoAction(native))
    registry.register(CursorPositionAction(native))
    registry.register(MoveCursorAction(native))
    registry.register(ClickAction(native))
    registry.register(TypeTextAction(native))

    if feature_set is None or "screen_perception" in feature_set:
        ocr = RapidOCREngine()
        registry.register(CaptureScreenAction(native))
        registry.register(ReadScreenAction(native, ocr))
        registry.register(FindTextOnScreenAction(native, ocr))

    return registry
