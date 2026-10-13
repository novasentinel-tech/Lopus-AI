"""Runtime central do Lopus-AI."""

from __future__ import annotations

from typing import Any

from lopus.actions import (
    ActionContext,
    ActionRegistry,
    ActionResult,
    Permission,
    PermissionStore,
    create_default_action_registry,
)
from lopus.agents.base import SYSTEM_PROMPT
from lopus.core.types import Message
from lopus.memory.session import SessionMemory
from lopus.models.base import ModelProvider


class LopusRuntime:
    def __init__(
        self,
        model: ModelProvider,
        memory: SessionMemory,
        *,
        actions: ActionRegistry | None = None,
        permissions: PermissionStore | None = None,
    ) -> None:
        self.model = model
        self.memory = memory
        self.actions = actions or create_default_action_registry()
        self.permissions = permissions or PermissionStore()

    def reply(self, user_input: str) -> str:
        text = user_input.strip()
        if not text:
            raise ValueError("A mensagem não pode ser vazia.")

        self.memory.add("user", text)
        messages = [Message("system", SYSTEM_PROMPT), *self.memory.snapshot()]
        answer = self.model.generate(messages).strip()
        self.memory.add("assistant", answer)
        return answer

    def execute_action(self, name: str, **kwargs: Any) -> ActionResult:
        context = ActionContext(permissions=self.permissions, actor="lopus")
        return self.actions.execute(name, context, **kwargs)

    def grant_permission(self, permission: Permission | str) -> None:
        self.permissions.grant(Permission(permission))

    def revoke_permission(self, permission: Permission | str) -> None:
        self.permissions.revoke(Permission(permission))

    def clear(self) -> None:
        self.memory.clear()

    def status(self) -> dict[str, object]:
        return {
            "provider": self.model.name,
            "messages_in_memory": len(self.memory),
            "memory_limit": self.memory.max_messages,
            "actions": self.actions.names(),
            "permissions": tuple(
                grant.permission.value for grant in self.permissions.snapshot()
            ),
        }
