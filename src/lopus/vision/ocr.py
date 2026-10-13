"""OCR local para leitura de texto visível na tela."""

from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Any, Iterable


class OCRUnavailableError(RuntimeError):
    """O motor OCR opcional não está disponível."""


@dataclass(frozen=True, slots=True)
class OCRRegion:
    text: str
    confidence: float
    box: tuple[tuple[int, int], ...]

    @property
    def center(self) -> tuple[int, int]:
        if not self.box:
            return (0, 0)
        xs = [point[0] for point in self.box]
        ys = [point[1] for point in self.box]
        return (round(sum(xs) / len(xs)), round(sum(ys) / len(ys)))

    def as_dict(self) -> dict[str, Any]:
        x, y = self.center
        return {
            "text": self.text,
            "confidence": round(self.confidence, 4),
            "box": [list(point) for point in self.box],
            "center": {"x": x, "y": y},
        }


class RapidOCREngine:
    """Wrapper lazy para RapidOCR.

    O pacote é opcional. O modelo só é carregado quando OCR é realmente usado.
    """

    def __init__(self) -> None:
        self._engine: Any | None = None
        self._import_error: str | None = None

    @property
    def available(self) -> bool:
        if self._engine is not None:
            return True
        try:
            from rapidocr import RapidOCR  # type: ignore
        except ImportError as exc:
            self._import_error = str(exc)
            return False
        self._engine = RapidOCR()
        return True

    @property
    def error(self) -> str | None:
        return self._import_error

    def _require(self) -> Any:
        if not self.available or self._engine is None:
            detail = f" ({self._import_error})" if self._import_error else ""
            raise OCRUnavailableError(
                "OCR local não está instalado. Instale com: pip install -e \".[vision]\""
                + detail
            )
        return self._engine

    @staticmethod
    def _as_list(value: Any) -> list[Any]:
        if value is None:
            return []
        if hasattr(value, "tolist"):
            value = value.tolist()
        if isinstance(value, tuple):
            return list(value)
        if isinstance(value, list):
            return value
        return [value]

    @staticmethod
    def _normalize_box(raw_box: Any) -> tuple[tuple[int, int], ...]:
        if hasattr(raw_box, "tolist"):
            raw_box = raw_box.tolist()
        if raw_box is None:
            return ()
        points: list[tuple[int, int]] = []
        for point in raw_box:
            if hasattr(point, "tolist"):
                point = point.tolist()
            if not isinstance(point, (list, tuple)) or len(point) < 2:
                continue
            points.append((round(float(point[0])), round(float(point[1]))))
        return tuple(points)

    def recognize(self, encoded_image: bytes, *, min_confidence: float = 0.35) -> tuple[OCRRegion, ...]:
        if not 0.0 <= min_confidence <= 1.0:
            raise ValueError("min_confidence deve estar entre 0 e 1.")
        engine = self._require()
        try:
            result = engine(encoded_image)
        except Exception as exc:
            raise OCRUnavailableError(f"Falha durante OCR local: {exc}") from exc

        txts = self._as_list(getattr(result, "txts", None))
        scores = self._as_list(getattr(result, "scores", None))
        boxes = self._as_list(getattr(result, "boxes", None))

        regions: list[OCRRegion] = []
        for text, score, box in zip(txts, scores, boxes, strict=False):
            normalized_text = str(text).strip()
            try:
                confidence = float(score)
            except (TypeError, ValueError):
                continue
            if not normalized_text or confidence < min_confidence:
                continue
            normalized_box = self._normalize_box(box)
            if not normalized_box:
                continue
            regions.append(
                OCRRegion(
                    text=normalized_text,
                    confidence=confidence,
                    box=normalized_box,
                )
            )
        return tuple(regions)

    @staticmethod
    def find(
        regions: Iterable[OCRRegion],
        query: str,
        *,
        limit: int = 5,
    ) -> tuple[OCRRegion, ...]:
        needle = query.strip().casefold()
        if not needle:
            return ()

        scored: list[tuple[float, OCRRegion]] = []
        for region in regions:
            haystack = region.text.casefold()
            if needle in haystack:
                score = 2.0 + region.confidence
            else:
                ratio = SequenceMatcher(None, needle, haystack).ratio()
                if ratio < 0.45:
                    continue
                score = ratio + region.confidence * 0.2
            scored.append((score, region))

        scored.sort(key=lambda item: item[0], reverse=True)
        return tuple(region for _, region in scored[: max(1, limit)])
