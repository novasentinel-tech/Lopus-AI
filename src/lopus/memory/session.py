"""Memória volátil da sessão atual."""

from __future__ import annotations

from lopus.core.types import Message


class SessionMemory:
    def __init__(self, max_messages: int = 24) -> None:
        if max_messages < 2:
            raise ValueError("max_messages deve ser >= 2")
        self.max_messages = max_messages
        self._messages: list[Message] = []

    def add(self, role: str, content: str) -> Message:
        if role not in {"user", "assistant"}:
            raise ValueError("A memória de sessão aceita apenas user ou assistant")
        message = Message(role=role, content=content.strip())  # type: ignore[arg-type]
        self._messages.append(message)
        self._trim()
        return message

    def snapshot(self) -> list[Message]:
        return list(self._messages)

    def clear(self) -> None:
        self._messages.clear()

    def __len__(self) -> int:
        return len(self._messages)

    def _trim(self) -> None:
        overflow = len(self._messages) - self.max_messages
        if overflow > 0:
            del self._messages[:overflow]
