"""Representação inicial da estrutura de documentos."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path


class DocumentKind(StrEnum):
    TEXT = "text"
    MARKDOWN = "markdown"
    DOCX = "docx"
    PDF = "pdf"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class DocumentSection:
    level: int
    title: str


@dataclass(slots=True)
class DocumentStructure:
    path: Path
    kind: DocumentKind
    sections: list[DocumentSection] = field(default_factory=list)


def detect_document_kind(path: str | Path) -> DocumentKind:
    suffix = Path(path).suffix.lower()
    return {
        ".txt": DocumentKind.TEXT,
        ".md": DocumentKind.MARKDOWN,
        ".docx": DocumentKind.DOCX,
        ".pdf": DocumentKind.PDF,
    }.get(suffix, DocumentKind.UNKNOWN)


def inspect_structure(path: str | Path) -> DocumentStructure:
    target = Path(path).expanduser().resolve()
    structure = DocumentStructure(path=target, kind=detect_document_kind(target))

    if structure.kind is DocumentKind.MARKDOWN and target.is_file():
        for line in target.read_text(encoding="utf-8").splitlines():
            stripped = line.lstrip()
            if not stripped.startswith("#"):
                continue
            level = len(stripped) - len(stripped.lstrip("#"))
            title = stripped[level:].strip()
            if title:
                structure.sections.append(DocumentSection(level=level, title=title))

    return structure
