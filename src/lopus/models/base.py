"""Contrato comum para providers de modelos."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence

from lopus.core.types import Message


class ModelError(RuntimeError):
    """Falha ao comunicar com ou executar um modelo."""


class ModelProvider(ABC):
    name: str

    @abstractmethod
    def generate(self, messages: Sequence[Message]) -> str:
        """Gera uma resposta a partir da conversa atual."""
        raise NotImplementedError
