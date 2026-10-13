"""Carregamento dos perfis de subagentes."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

PROFILE_DIR = Path(__file__).with_name("models-subagents")


@dataclass(frozen=True, slots=True)
class SubagentProfile:
    name: str
    purpose: str
    system_instruction: str
    action_groups: tuple[str, ...] = ()


def available_profiles() -> tuple[str, ...]:
    return tuple(sorted(path.stem for path in PROFILE_DIR.glob("*.json")))


def load_profile(name: str) -> SubagentProfile:
    normalized = name.strip().lower().replace(" ", "_")
    path = PROFILE_DIR / f"{normalized}.json"
    if not path.is_file():
        raise KeyError(f"Perfil de subagente não encontrado: {normalized}")

    data = json.loads(path.read_text(encoding="utf-8"))
    return SubagentProfile(
        name=data["name"],
        purpose=data["purpose"],
        system_instruction=data["system_instruction"],
        action_groups=tuple(data.get("action_groups", ())),
    )
