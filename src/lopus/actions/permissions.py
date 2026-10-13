"""Armazenamento simples de permissões para o primeiro runtime de ações."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Iterable

from lopus.actions.base import Permission


class PermissionDeniedError(PermissionError):
    pass


@dataclass(frozen=True, slots=True)
class PermissionGrant:
    permission: Permission
    granted_at: datetime
    granted_by: str = "user"


class PermissionStore:
    def __init__(self, permissions: Iterable[Permission] = ()) -> None:
        now = datetime.now(UTC)
        self._grants = {
            permission: PermissionGrant(permission=permission, granted_at=now)
            for permission in permissions
        }

    def grant(self, permission: Permission, *, granted_by: str = "user") -> None:
        self._grants[permission] = PermissionGrant(
            permission=permission,
            granted_at=datetime.now(UTC),
            granted_by=granted_by,
        )

    def revoke(self, permission: Permission) -> None:
        self._grants.pop(permission, None)

    def has(self, permission: Permission) -> bool:
        return permission in self._grants

    def require(self, *permissions: Permission) -> None:
        missing = [permission.value for permission in permissions if not self.has(permission)]
        if missing:
            raise PermissionDeniedError(
                "Permissão necessária não concedida: " + ", ".join(missing)
            )

    def snapshot(self) -> tuple[PermissionGrant, ...]:
        return tuple(sorted(self._grants.values(), key=lambda grant: grant.permission.value))
