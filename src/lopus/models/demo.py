"""Provider local de demonstração, sem LLM."""

from __future__ import annotations

from collections.abc import Sequence

from lopus.core.types import Message
from lopus.models.base import ModelProvider


class DemoProvider(ModelProvider):
    name = "demo"

    def generate(self, messages: Sequence[Message]) -> str:
        user_messages = [message.content for message in messages if message.role == "user"]
        latest = user_messages[-1] if user_messages else ""
        return (
            "Modo demo ativo. O runtime recebeu sua mensagem corretamente, mas nenhum modelo de IA "
            "está conectado ainda.\n\n"
            f"Última entrada: {latest}\n\n"
            "Para usar um modelo local, configure LOPUS_PROVIDER=ollama e escolha um modelo em LOPUS_MODEL."
        )
