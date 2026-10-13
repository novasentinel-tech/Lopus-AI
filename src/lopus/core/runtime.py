"""Primeiro runtime funcional do Lopus-AI."""

from __future__ import annotations

from lopus.agents.base import SYSTEM_PROMPT
from lopus.core.types import Message
from lopus.memory.session import SessionMemory
from lopus.models.base import ModelProvider


class LopusRuntime:
    def __init__(self, model: ModelProvider, memory: SessionMemory) -> None:
        self.model = model
        self.memory = memory

    def reply(self, user_input: str) -> str:
        text = user_input.strip()
        if not text:
            raise ValueError("A mensagem não pode ser vazia.")

        self.memory.add("user", text)
        messages = [Message("system", SYSTEM_PROMPT), *self.memory.snapshot()]
        answer = self.model.generate(messages).strip()
        self.memory.add("assistant", answer)
        return answer

    def clear(self) -> None:
        self.memory.clear()

    def status(self) -> dict[str, object]:
        return {
            "provider": self.model.name,
            "messages_in_memory": len(self.memory),
            "memory_limit": self.memory.max_messages,
        }
