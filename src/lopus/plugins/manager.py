"""Descoberta de plugins baseada em manifestos JSON."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class PluginManifest:
    id: str
    name: str
    description: str
    version: str
    permissions: tuple[str, ...]


def _project_root() -> Path:
    configured = os.getenv("LOPUS_PROJECT_ROOT")
    if configured:
        return Path(configured).expanduser().resolve()
    candidates = [Path.cwd(), *Path.cwd().parents, Path(__file__).resolve().parents[3]]
    for candidate in candidates:
        if (candidate / "plugins").is_dir():
            return candidate
    return Path.cwd()


class PluginManager:
    def __init__(self, directory: Path | None = None) -> None:
        self.directory = directory or (_project_root() / "plugins")

    def discover(self) -> tuple[PluginManifest, ...]:
        if not self.directory.is_dir():
            return ()
        found: list[PluginManifest] = []
        for manifest_path in sorted(self.directory.glob("*/manifest.json")):
            try:
                data = json.loads(manifest_path.read_text(encoding="utf-8"))
                found.append(PluginManifest(id=str(data["id"]), name=str(data["name"]), description=str(data.get("description", "")), version=str(data.get("version", "0.0.0")), permissions=tuple(data.get("permissions", ()))))
            except (OSError, json.JSONDecodeError, KeyError, TypeError):
                continue
        return tuple(found)
