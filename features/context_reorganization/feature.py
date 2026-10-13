"""Estruturas iniciais da feature de reorganização de contexto."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ContextBlock:
    category: str
    content: str
    priority: int = 0


@dataclass(slots=True)
class ReorganizedContext:
    active: list[ContextBlock] = field(default_factory=list)
    archived: list[ContextBlock] = field(default_factory=list)


class ContextReorganizationFeature:
    """Contrato inicial; a estratégia inteligente será implementada depois."""

    def reorganize(self, blocks: list[ContextBlock]) -> ReorganizedContext:
        ordered = sorted(blocks, key=lambda block: block.priority, reverse=True)
        return ReorganizedContext(active=ordered)
