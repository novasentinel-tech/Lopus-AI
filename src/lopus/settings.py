"""Persistência local das configurações do Lopus-AI."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class AppSettings:
    setup_complete: bool = False
    provider: str = "demo"
    model: str = "llama3.2:3b"
    enabled_features: list[str] = field(default_factory=list)
    enabled_plugins: list[str] = field(default_factory=list)
    granted_permissions: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AppSettings":
        return cls(
            setup_complete=bool(data.get("setup_complete", False)),
            provider=str(data.get("provider", "demo")),
            model=str(data.get("model", "llama3.2:3b")),
            enabled_features=list(data.get("enabled_features", [])),
            enabled_plugins=list(data.get("enabled_plugins", [])),
            granted_permissions=list(data.get("granted_permissions", [])),
        )


class SettingsStore:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or Path.home() / ".lopus" / "settings.json"

    def load(self) -> AppSettings:
        if not self.path.exists():
            return AppSettings()
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return AppSettings()
        return AppSettings.from_dict(data)

    def save(self, settings: AppSettings) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = self.path.with_suffix(".tmp")
        temp_path.write_text(
            json.dumps(asdict(settings), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        temp_path.replace(self.path)
