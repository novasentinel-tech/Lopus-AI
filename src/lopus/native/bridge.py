"""Wrapper estável em Python para a extensão C++ `lopus_native`."""

from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
from types import ModuleType
from typing import Any


class NativeBackendUnavailableError(RuntimeError):
    """A extensão nativa não está disponível nesta instalação."""


class NativeOperationError(RuntimeError):
    """O backend existe, mas a operação nativa falhou ou não é suportada."""


@dataclass(frozen=True, slots=True)
class NativeCapabilities:
    available: bool
    platform: str
    process_id: int | None
    gui_input_supported: bool
    primary_screen_size: tuple[int, int] | None
    backend_version: str | None
    error: str | None = None


class NativeBridge:
    """Isola o restante do Lopus do módulo binário compilado."""

    def __init__(self, module: ModuleType | Any | None = None) -> None:
        self._module = module
        self._import_error: str | None = None
        if module is None:
            try:
                self._module = import_module("lopus_native")
            except ImportError as exc:
                self._module = None
                self._import_error = str(exc)

    @property
    def available(self) -> bool:
        return self._module is not None

    @property
    def import_error(self) -> str | None:
        return self._import_error

    def _require(self) -> Any:
        if self._module is None:
            detail = f" ({self._import_error})" if self._import_error else ""
            raise NativeBackendUnavailableError(
                "O Lopus Native Core não foi carregado. Reinstale o projeto para "
                f"compilar a extensão C++{detail}."
            )
        return self._module

    def platform_name(self) -> str:
        return str(self._require().platform_name())

    def process_id(self) -> int:
        return int(self._require().process_id())

    def gui_input_supported(self) -> bool:
        return bool(self._require().gui_input_supported())

    def cursor_position(self) -> tuple[int, int]:
        try:
            x, y = self._require().cursor_position()
            return int(x), int(y)
        except NativeBackendUnavailableError:
            raise
        except Exception as exc:
            raise NativeOperationError(str(exc)) from exc

    def move_cursor(self, x: int, y: int) -> None:
        try:
            self._require().move_cursor(int(x), int(y))
        except NativeBackendUnavailableError:
            raise
        except Exception as exc:
            raise NativeOperationError(str(exc)) from exc

    def primary_screen_size(self) -> tuple[int, int]:
        try:
            width, height = self._require().primary_screen_size()
            return int(width), int(height)
        except NativeBackendUnavailableError:
            raise
        except Exception as exc:
            raise NativeOperationError(str(exc)) from exc

    def capabilities(self) -> NativeCapabilities:
        if not self.available:
            return NativeCapabilities(
                available=False,
                platform="unknown",
                process_id=None,
                gui_input_supported=False,
                primary_screen_size=None,
                backend_version=None,
                error=self._import_error,
            )

        module = self._require()
        platform = self.platform_name()
        gui_supported = self.gui_input_supported()
        screen_size: tuple[int, int] | None = None
        if gui_supported:
            try:
                screen_size = self.primary_screen_size()
            except NativeOperationError:
                screen_size = None

        return NativeCapabilities(
            available=True,
            platform=platform,
            process_id=self.process_id(),
            gui_input_supported=gui_supported,
            primary_screen_size=screen_size,
            backend_version=str(getattr(module, "__version__", "unknown")),
            error=None,
        )
