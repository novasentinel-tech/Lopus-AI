"""Criação do runtime a partir das configurações persistidas do painel."""

from __future__ import annotations

from lopus.actions import Permission, PermissionStore, create_default_action_registry
from lopus.config import LopusConfig
from lopus.core.runtime import LopusRuntime
from lopus.memory.session import SessionMemory
from lopus.models.factory import create_model
from lopus.settings import AppSettings


def runtime_from_settings(settings: AppSettings) -> LopusRuntime:
    config = LopusConfig.from_env().with_overrides(
        provider=settings.provider,
        model=settings.model,
    )
    permissions = []
    for value in settings.granted_permissions:
        try:
            permissions.append(Permission(value))
        except ValueError:
            continue

    actions = create_default_action_registry(enabled_features=settings.enabled_features)
    return LopusRuntime(
        model=create_model(config),
        memory=SessionMemory(max_messages=config.max_messages),
        permissions=PermissionStore(permissions),
        actions=actions,
    )
