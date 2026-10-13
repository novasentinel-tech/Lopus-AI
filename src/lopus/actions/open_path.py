"""Ação de alto nível para abrir arquivos e pastas."""

from __future__ import annotations

import os
import subprocess
import sys
from enum import StrEnum
from pathlib import Path
from typing import Protocol

from lopus.actions.base import Action, ActionContext, ActionError, ActionResult, Permission
from lopus.actions.shell import Command, RunCommandAction


class OpenMethod(StrEnum):
    AUTO = "auto"
    NATIVE = "native"
    SHELL = "shell"
    GUI = "gui"


class GuiPathController(Protocol):
    def open_path(self, path: str) -> None: ...


class OpenPathAction(Action):
    name = "file.open"
    description = "Abre um arquivo ou pasta local no aplicativo padrão do sistema."
    required_permissions = frozenset({Permission.FILE_OPEN})
    agent_exposed = True
    parameters_schema = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Caminho local do arquivo ou pasta."},
            "method": {
                "type": "string",
                "enum": ["auto", "native"],
                "default": "auto",
                "description": "Para o agente, apenas abertura nativa é exposta por segurança.",
            },
        },
        "required": ["path"],
        "additionalProperties": False,
    }

    def __init__(
        self,
        *,
        shell_action: RunCommandAction | None = None,
        gui_controller: GuiPathController | None = None,
    ) -> None:
        self.shell_action = shell_action or RunCommandAction()
        self.gui_controller = gui_controller

    def execute(
        self,
        context: ActionContext,
        *,
        path: str,
        method: OpenMethod | str = OpenMethod.AUTO,
    ) -> ActionResult:
        target = Path(path).expanduser().resolve()
        if not target.exists():
            raise ActionError(f"Caminho não encontrado: {target}")

        selected = OpenMethod(method)
        if selected in {OpenMethod.AUTO, OpenMethod.NATIVE}:
            self._open_native(target)
            return ActionResult(
                success=True,
                action=self.name,
                message="Caminho enviado ao aplicativo padrão do sistema.",
                data={"path": str(target), "method": OpenMethod.NATIVE.value},
            )

        if selected is OpenMethod.SHELL:
            context.permissions.require(Permission.SHELL_EXECUTE)
            command = self._shell_command(target)
            result = self.shell_action.execute(context, command=command)
            return ActionResult(
                success=result.success,
                action=self.name,
                message=result.message,
                data={"path": str(target), "method": "shell", **dict(result.data)},
            )

        context.permissions.require(Permission.GUI_CONTROL)
        if self.gui_controller is None:
            raise ActionError("Nenhum controlador gráfico foi conectado ao OpenPathAction.")
        self.gui_controller.open_path(str(target))
        return ActionResult(
            success=True,
            action=self.name,
            message="Solicitação enviada ao controlador gráfico.",
            data={"path": str(target), "method": OpenMethod.GUI.value},
        )

    @staticmethod
    def _open_native(path: Path) -> None:
        if os.name == "nt":
            os.startfile(str(path))  # type: ignore[attr-defined]
            return
        if sys.platform == "darwin":
            subprocess.Popen(["open", str(path)])
            return
        subprocess.Popen(["xdg-open", str(path)])

    @staticmethod
    def _shell_command(path: Path) -> Command:
        escaped = str(path).replace("'", "''")
        if os.name == "nt":
            return Command.powershell(f"Start-Process -FilePath '{escaped}'")
        shell_path = str(path).replace("'", "'\"'\"'")
        if sys.platform == "darwin":
            return Command.bash(f"open '{shell_path}'")
        return Command.bash(f"xdg-open '{shell_path}'")
