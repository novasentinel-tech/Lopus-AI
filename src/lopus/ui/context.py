"""Dependências compartilhadas pela interface gráfica."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from lopus.features import FeatureManager
from lopus.models.manager import OllamaManager
from lopus.plugins import PluginManager
from lopus.settings import AppSettings, SettingsStore


@dataclass(slots=True)
class UIContext:
    settings_store: SettingsStore
    settings: AppSettings
    ollama: OllamaManager
    features: FeatureManager
    plugins: PluginManager

    def save(self) -> None:
        self.settings_store.save(self.settings)


@lru_cache(maxsize=1)
def get_ui_context() -> UIContext:
    store = SettingsStore()
    return UIContext(settings_store=store, settings=store.load(), ollama=OllamaManager(), features=FeatureManager(), plugins=PluginManager())
