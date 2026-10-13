"""Actions que usam o Lopus Native Core para operações de baixo nível."""

from __future__ import annotations

from typing import Any

from lopus.actions.base import Action, ActionContext, ActionError, ActionResult, Permission
from lopus.native import NativeBackendUnavailableError, NativeBridge, NativeOperationError


class NativeSystemInfoAction(Action):
    name = "system.native_info"
    description = "Consulta o estado e capacidades do backend C++ do Lopus."
    agent_exposed = True

    def __init__(self, bridge: NativeBridge | None = None) -> None:
        self.bridge = bridge or NativeBridge()

    def execute(self, context: ActionContext, **kwargs: Any) -> ActionResult:
        del context, kwargs
        capabilities = self.bridge.capabilities()
        return ActionResult(
            success=capabilities.available,
            action=self.name,
            message=("Lopus Native Core disponível." if capabilities.available else "Lopus Native Core indisponível."),
            data={
                "available": capabilities.available,
                "platform": capabilities.platform,
                "process_id": capabilities.process_id,
                "gui_input_supported": capabilities.gui_input_supported,
                "screen_capture_supported": capabilities.screen_capture_supported,
                "primary_screen_size": capabilities.primary_screen_size,
                "backend_version": capabilities.backend_version,
                "error": capabilities.error,
            },
        )


class CursorPositionAction(Action):
    name = "gui.cursor_position"
    description = "Lê a posição atual do cursor do sistema."
    required_permissions = frozenset({Permission.GUI_CONTROL})
    agent_exposed = True

    def __init__(self, bridge: NativeBridge | None = None) -> None:
        self.bridge = bridge or NativeBridge()

    def execute(self, context: ActionContext, **kwargs: Any) -> ActionResult:
        del context, kwargs
        try:
            x, y = self.bridge.cursor_position()
        except (NativeBackendUnavailableError, NativeOperationError) as exc:
            raise ActionError(str(exc)) from exc
        return ActionResult(True, self.name, "Posição do cursor obtida.", {"x": x, "y": y})


class MoveCursorAction(Action):
    name = "gui.move_cursor"
    description = "Move o cursor do sistema para uma coordenada absoluta da tela."
    required_permissions = frozenset({Permission.GUI_CONTROL})
    agent_exposed = True
    parameters_schema = {
        "type": "object",
        "properties": {
            "x": {"type": "integer", "description": "Coordenada horizontal absoluta."},
            "y": {"type": "integer", "description": "Coordenada vertical absoluta."},
        },
        "required": ["x", "y"],
        "additionalProperties": False,
    }

    def __init__(self, bridge: NativeBridge | None = None) -> None:
        self.bridge = bridge or NativeBridge()

    def execute(self, context: ActionContext, *, x: int, y: int, **kwargs: Any) -> ActionResult:
        del context, kwargs
        if isinstance(x, bool) or isinstance(y, bool):
            raise ActionError("As coordenadas do cursor devem ser números inteiros.")
        try:
            target_x, target_y = int(x), int(y)
            width, height = self.bridge.primary_screen_size()
            if not (0 <= target_x < width and 0 <= target_y < height):
                raise ActionError(f"Coordenada fora da tela principal ({width}x{height}).")
            self.bridge.move_cursor(target_x, target_y)
        except (TypeError, ValueError) as exc:
            raise ActionError("As coordenadas do cursor devem ser números inteiros.") from exc
        except (NativeBackendUnavailableError, NativeOperationError) as exc:
            raise ActionError(str(exc)) from exc
        return ActionResult(True, self.name, "Cursor movido.", {"x": target_x, "y": target_y})


class ClickAction(Action):
    name = "gui.click"
    description = "Move o cursor para uma coordenada e executa um clique do mouse."
    required_permissions = frozenset({Permission.GUI_CONTROL})
    agent_exposed = True
    parameters_schema = {
        "type": "object",
        "properties": {
            "x": {"type": "integer"},
            "y": {"type": "integer"},
            "button": {"type": "string", "enum": ["left", "right", "middle"], "default": "left"},
        },
        "required": ["x", "y"],
        "additionalProperties": False,
    }

    def __init__(self, bridge: NativeBridge | None = None) -> None:
        self.bridge = bridge or NativeBridge()

    def execute(self, context: ActionContext, *, x: int, y: int, button: str = "left", **kwargs: Any) -> ActionResult:
        del context, kwargs
        try:
            width, height = self.bridge.primary_screen_size()
            x, y = int(x), int(y)
            if not (0 <= x < width and 0 <= y < height):
                raise ActionError(f"Coordenada fora da tela principal ({width}x{height}).")
            self.bridge.move_cursor(x, y)
            self.bridge.click_mouse(button)
        except (NativeBackendUnavailableError, NativeOperationError) as exc:
            raise ActionError(str(exc)) from exc
        return ActionResult(True, self.name, "Clique executado.", {"x": x, "y": y, "button": button})


class TypeTextAction(Action):
    name = "gui.type_text"
    description = "Digita texto Unicode no elemento atualmente focado."
    required_permissions = frozenset({Permission.KEYBOARD_CONTROL})
    agent_exposed = True
    parameters_schema = {
        "type": "object",
        "properties": {"text": {"type": "string", "description": "Texto exato a digitar."}},
        "required": ["text"],
        "additionalProperties": False,
    }

    def __init__(self, bridge: NativeBridge | None = None) -> None:
        self.bridge = bridge or NativeBridge()

    def execute(self, context: ActionContext, *, text: str, **kwargs: Any) -> ActionResult:
        del context, kwargs
        if not isinstance(text, str):
            raise ActionError("O texto precisa ser uma string.")
        try:
            self.bridge.type_text(text)
        except (NativeBackendUnavailableError, NativeOperationError) as exc:
            raise ActionError(str(exc)) from exc
        return ActionResult(True, self.name, "Texto digitado pelo backend nativo.", {"characters": len(text)})
