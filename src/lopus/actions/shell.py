"""Ações para execução controlada de comandos locais."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass

from lopus.actions.base import Action, ActionContext, ActionResult, Permission


@dataclass(frozen=True, slots=True)
class Command:
    executable: str
    arguments: tuple[str, ...] = ()

    @classmethod
    def powershell(cls, script: str) -> "Command":
        return cls(
            executable="powershell.exe",
            arguments=("-NoProfile", "-NonInteractive", "-Command", script),
        )

    @classmethod
    def bash(cls, script: str) -> "Command":
        return cls(executable="bash", arguments=("-lc", script))


class RunCommandAction(Action):
    name = "system.run_command"
    description = "Executa um comando local explicitamente autorizado."
    required_permissions = frozenset({Permission.SHELL_EXECUTE})

    def __init__(self, *, timeout: float = 30.0) -> None:
        self.timeout = timeout

    def execute(
        self,
        context: ActionContext,
        *,
        command: Command,
        cwd: str | None = None,
    ) -> ActionResult:
        process = subprocess.run(
            [command.executable, *command.arguments],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=self.timeout,
            check=False,
            shell=False,
        )
        return ActionResult(
            success=process.returncode == 0,
            action=self.name,
            message=f"Comando finalizado com código {process.returncode}.",
            data={
                "returncode": process.returncode,
                "stdout": process.stdout,
                "stderr": process.stderr,
            },
        )
