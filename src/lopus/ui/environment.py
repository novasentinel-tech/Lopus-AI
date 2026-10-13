"""Detecção do ambiente usado para iniciar a interface do Lopus-AI."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Mapping

_TRUTHY = {"1", "true", "yes", "on"}


@dataclass(frozen=True, slots=True)
class UILaunchConfig:
    mode: str
    native: bool
    host: str
    port: int
    show_browser: bool


class UIEnvironment:
    """Resolve como o painel deve ser iniciado sem espalhar lógica de ambiente pela UI."""

    @staticmethod
    def is_codespaces(env: Mapping[str, str] | None = None) -> bool:
        source = env if env is not None else os.environ
        explicit = source.get("CODESPACES", "").strip().lower() in _TRUTHY
        forwarding_domain = bool(
            source.get("GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN", "").strip()
        )
        return explicit or forwarding_domain

    @classmethod
    def launch_config(
        cls,
        env: Mapping[str, str] | None = None,
    ) -> UILaunchConfig:
        source = env if env is not None else os.environ
        raw_port = source.get("LOPUS_UI_PORT", "8080").strip() or "8080"

        try:
            port = int(raw_port)
        except ValueError as exc:
            raise ValueError("LOPUS_UI_PORT deve ser um número inteiro.") from exc

        if not 1 <= port <= 65535:
            raise ValueError("LOPUS_UI_PORT deve estar entre 1 e 65535.")

        if cls.is_codespaces(source):
            return UILaunchConfig(
                mode="codespaces",
                native=False,
                host="0.0.0.0",
                port=port,
                show_browser=False,
            )

        return UILaunchConfig(
            mode="local",
            native=True,
            host="127.0.0.1",
            port=port,
            show_browser=False,
        )
