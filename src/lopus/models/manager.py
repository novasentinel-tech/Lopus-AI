"""Gerenciamento local de modelos disponíveis através do Ollama."""

from __future__ import annotations

import asyncio
import json
import shutil
from dataclasses import dataclass
from urllib.error import URLError
from urllib.request import urlopen


class OllamaUnavailableError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class InstalledModel:
    name: str
    size: int

    @property
    def size_gb(self) -> float:
        return self.size / (1024 ** 3)


class OllamaManager:
    def __init__(self, base_url: str = "http://127.0.0.1:11434") -> None:
        self.base_url = base_url.rstrip("/")

    @property
    def executable(self) -> str | None:
        return shutil.which("ollama")

    def is_installed(self) -> bool:
        return self.executable is not None

    def is_running(self) -> bool:
        try:
            with urlopen(f"{self.base_url}/api/tags", timeout=1.5):
                return True
        except (OSError, URLError):
            return False

    def list_installed(self) -> tuple[InstalledModel, ...]:
        try:
            with urlopen(f"{self.base_url}/api/tags", timeout=3.0) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except (OSError, URLError, json.JSONDecodeError) as exc:
            raise OllamaUnavailableError("Não foi possível consultar o Ollama local.") from exc
        models: list[InstalledModel] = []
        for item in payload.get("models", []):
            name = str(item.get("name", "")).strip()
            if name:
                models.append(InstalledModel(name=name, size=int(item.get("size", 0) or 0)))
        return tuple(models)

    async def pull(self, model: str, on_status=None) -> None:
        executable = self.executable
        if executable is None:
            raise OllamaUnavailableError("O executável do Ollama não foi encontrado no computador.")
        process = await asyncio.create_subprocess_exec(executable, "pull", model, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT)
        assert process.stdout is not None
        while True:
            raw = await process.stdout.readline()
            if not raw:
                break
            line = raw.decode(errors="replace").strip()
            if line and on_status is not None:
                on_status(line)
        return_code = await process.wait()
        if return_code != 0:
            raise RuntimeError(f"Ollama encerrou o download com código {return_code}.")
