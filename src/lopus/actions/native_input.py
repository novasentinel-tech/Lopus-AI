"""Actions que usam o Lopus Native Core para operações de baixo nível."""

from __future__ import annotations

from typing import Any

from lopus.actions.base import Action, ActionContext, ActionError, ActionResult, Permission
from lopus.native import (
    NativeBackendUnavailableError,
    NativeBridge,
    NativeOperationError,
)


class NativeSystemInfoAction(Action):
    name = "system.native_info"
    description = "Consulta o estado e capacidades do backend C++ do Lopus."

    def __init__(self, bridge: NativeBridge | None = None) -> None:
        self.bridge = bridge or NativeBridge()

    def execute(self, context: ActionContext, **kwargs: Any) -> ActionResult:
        del context, kwargs
        capabilities = self.bridge.capabilities()
        return ActionResult(
            success=capabilities.available,
            action=self.name,
            message=(
                "Lopus Native Core disponível."
                if capabilities.available
                else "Lopus Native Core indisponível."
            ),
            data={
                "available": capabilities.available,
                "platform": capabilities.platform,
                "process_id": capabilities.process_id,
                "gui_input_supported": capabilities.gui_input_supported,
                "primary_screen_size": capabilities.primary_screen_size,
                "backend_version": capabilities.backend_version,
                "error": capabilities.error,
            },
        )


class CursorPositionAction(Action):
    name = "gui.cursor_position"
    description = "Lê a posição atual do cursor pelo backend nativo."
    required_permissions = frozenset({Permission.GUI_CONTROL})

    def __init__(self, bridge: NativeBridge | None = None) -> None:
        self.bridge = bridge or NativeBridge()

    def execute(self, context: ActionContext, **kwargs: Any) -> ActionResult:
        del context, kwargs
        try:
            x, y = self.bridge.cursor_position()
        except (NativeBackendUnavailableError, NativeOperationError) as exc:
            raise ActionError(str(exc)) from exc
        return ActionResult(
            success=True,
            action=self.name,
            message="Posição do cursor obtida pelo backend nativo.",
            data={"x": x, "y": y},
        )


class MoveCursorAction(Action):
    name = "gui.move_cursor"
    description = "Move o cursor do sistema usando o backend C++."
    required_permissions = frozenset({Permission.GUI_CONTROL})

    def __init__(self, bridge: NativeBridge | None = None) -> None:
        self.bridge = bridge or NativeBridge()

    def execute(
        self,
        context: ActionContext,
        *,
        x: int,
        y: int,
        **kwargs: Any,
    ) -> ActionResult:
        del context, kwargs
        if isinstance(x, bool) or isinstance(y, bool):
            raise ActionError("As coordenadas do cursor devem ser números inteiros.")
        try:
            target_x = int(x)
            target_y = int(y)
            self.bridge.move_cursor(target_x, target_y)
        except (TypeError, ValueError) as exc:
            raise ActionError("As coordenadas do cursor devem ser números inteiros.") from exc
        except (NativeBackendUnavailableError, NativeOperationError) as exc:
            raise ActionError(str(exc)) from exc

        return ActionResult(
            success=True,
            action=self.name,
            message="Cursor movido pelo backend nativo.",
            data={"x": target_x, "y": target_y},
        )
