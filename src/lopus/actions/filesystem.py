"""Ações utilitárias para arquivos e diretórios."""

from __future__ import annotations

from pathlib import Path

from lopus.actions.base import Action, ActionContext, ActionError, ActionResult, Permission


class InspectPathAction(Action):
    name = "file.inspect"
    description = "Inspeciona metadados básicos de um caminho local."
    required_permissions = frozenset({Permission.FILE_READ})

    def execute(self, context: ActionContext, *, path: str) -> ActionResult:
        target = Path(path).expanduser().resolve()
        if not target.exists():
            raise ActionError(f"Caminho não encontrado: {target}")

        return ActionResult(
            success=True,
            action=self.name,
            message="Caminho inspecionado.",
            data={
                "path": str(target),
                "name": target.name,
                "suffix": target.suffix.lower(),
                "is_file": target.is_file(),
                "is_directory": target.is_dir(),
                "size": target.stat().st_size if target.is_file() else None,
            },
        )


class ReadTextFileAction(Action):
    name = "file.read_text"
    description = "Lê um arquivo de texto local dentro do limite configurado."
    required_permissions = frozenset({Permission.FILE_READ})

    def __init__(self, *, max_bytes: int = 1_000_000) -> None:
        self.max_bytes = max_bytes

    def execute(
        self,
        context: ActionContext,
        *,
        path: str,
        encoding: str = "utf-8",
    ) -> ActionResult:
        target = Path(path).expanduser().resolve()
        if not target.is_file():
            raise ActionError(f"Arquivo não encontrado: {target}")
        if target.stat().st_size > self.max_bytes:
            raise ActionError(
                f"Arquivo excede o limite de {self.max_bytes} bytes para leitura textual."
            )

        content = target.read_text(encoding=encoding)
        return ActionResult(
            success=True,
            action=self.name,
            message="Arquivo lido.",
            data={"path": str(target), "content": content, "encoding": encoding},
        )


class WriteTextFileAction(Action):
    name = "file.write_text"
    description = "Cria ou substitui um arquivo de texto quando autorizado."
    required_permissions = frozenset({Permission.FILE_WRITE})

    def execute(
        self,
        context: ActionContext,
        *,
        path: str,
        content: str,
        encoding: str = "utf-8",
        overwrite: bool = False,
    ) -> ActionResult:
        target = Path(path).expanduser().resolve()
        if target.exists() and not overwrite:
            raise ActionError(
                "O arquivo já existe. Defina overwrite=True para substituir explicitamente."
            )
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding=encoding)

        return ActionResult(
            success=True,
            action=self.name,
            message="Arquivo gravado.",
            data={"path": str(target), "bytes": target.stat().st_size},
        )
