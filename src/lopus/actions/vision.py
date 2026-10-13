"""Actions de percepção visual: captura de tela, OCR e interação assistida."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from lopus.actions.base import Action, ActionContext, ActionError, ActionResult, Permission
from lopus.native import NativeBackendUnavailableError, NativeBridge, NativeOperationError
from lopus.vision import OCRUnavailableError, RapidOCREngine


class _ScreenOCRMixin:
    bridge: NativeBridge
    ocr: RapidOCREngine

    def _read_regions(self, min_confidence: float):
        try:
            bmp = self.bridge.capture_primary_screen_bmp()
            regions = self.ocr.recognize(bmp, min_confidence=float(min_confidence))
            return regions
        except (NativeBackendUnavailableError, NativeOperationError, OCRUnavailableError) as exc:
            raise ActionError(str(exc)) from exc


class CaptureScreenAction(Action):
    name = "screen.capture"
    description = "Captura a tela principal e salva uma imagem BMP local para inspeção."
    required_permissions = frozenset({Permission.SCREEN_CAPTURE})
    agent_exposed = False

    def __init__(self, bridge: NativeBridge | None = None) -> None:
        self.bridge = bridge or NativeBridge()

    def execute(self, context: ActionContext, *, path: str | None = None, **kwargs: Any) -> ActionResult:
        del context, kwargs
        try:
            bmp = self.bridge.capture_primary_screen_bmp()
            width, height = self.bridge.primary_screen_size()
        except (NativeBackendUnavailableError, NativeOperationError) as exc:
            raise ActionError(str(exc)) from exc

        if path is None:
            stamp = datetime.now(UTC).strftime("%Y%m%d-%H%M%S-%f")
            target = Path.home() / ".lopus" / "captures" / f"screen-{stamp}.bmp"
        else:
            target = Path(path).expanduser().resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(bmp)
        return ActionResult(
            True,
            self.name,
            "Tela capturada.",
            {"path": str(target), "width": width, "height": height, "bytes": len(bmp)},
        )


class ReadScreenAction(_ScreenOCRMixin, Action):
    name = "vision.read_screen"
    description = (
        "Observa a tela atual com OCR local e retorna textos visíveis, confiança e coordenadas. "
        "Use quando precisar entender o estado geral da interface."
    )
    required_permissions = frozenset({Permission.SCREEN_CAPTURE})
    agent_exposed = True
    parameters_schema = {
        "type": "object",
        "properties": {
            "min_confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0, "default": 0.45},
            "max_regions": {"type": "integer", "minimum": 1, "maximum": 200, "default": 120},
        },
        "additionalProperties": False,
    }

    def __init__(self, bridge: NativeBridge | None = None, ocr: RapidOCREngine | None = None) -> None:
        self.bridge = bridge or NativeBridge()
        self.ocr = ocr or RapidOCREngine()

    def execute(self, context: ActionContext, *, min_confidence: float = 0.45, max_regions: int = 120, **kwargs: Any) -> ActionResult:
        del context, kwargs
        regions = self._read_regions(min_confidence)
        try:
            width, height = self.bridge.primary_screen_size()
        except (NativeBackendUnavailableError, NativeOperationError) as exc:
            raise ActionError(str(exc)) from exc
        limited = regions[: max(1, min(int(max_regions), 200))]
        return ActionResult(
            True,
            self.name,
            f"Tela observada: {len(limited)} regiões de texto reconhecidas.",
            {
                "screen": {"width": width, "height": height},
                "text": "\n".join(region.text for region in limited),
                "regions": [region.as_dict() for region in limited],
                "truncated": len(regions) > len(limited),
            },
        )


class FindTextOnScreenAction(_ScreenOCRMixin, Action):
    name = "vision.find_text"
    description = (
        "Procura um texto na tela atual usando OCR e devolve candidatos com coordenadas centrais. "
        "Use quando precisar localizar um elemento antes de interagir."
    )
    required_permissions = frozenset({Permission.SCREEN_CAPTURE})
    agent_exposed = True
    parameters_schema = {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Texto ou rótulo visual a localizar."},
            "limit": {"type": "integer", "minimum": 1, "maximum": 10, "default": 5},
            "min_confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0, "default": 0.35},
        },
        "required": ["query"],
        "additionalProperties": False,
    }

    def __init__(self, bridge: NativeBridge | None = None, ocr: RapidOCREngine | None = None) -> None:
        self.bridge = bridge or NativeBridge()
        self.ocr = ocr or RapidOCREngine()

    def execute(self, context: ActionContext, *, query: str, limit: int = 5, min_confidence: float = 0.35, **kwargs: Any) -> ActionResult:
        del context, kwargs
        if not query.strip():
            raise ActionError("Informe um texto para procurar na tela.")
        regions = self._read_regions(min_confidence)
        matches = self.ocr.find(regions, query, limit=max(1, min(int(limit), 10)))
        return ActionResult(
            True,
            self.name,
            f"Busca visual concluída: {len(matches)} candidato(s) para '{query}'.",
            {"query": query, "matches": [region.as_dict() for region in matches]},
        )


class ClickTextAction(_ScreenOCRMixin, Action):
    name = "vision.click_text"
    description = (
        "Localiza um rótulo textual por OCR e clica no centro do melhor candidato. "
        "Prefira esta ação quando o rótulo visual é claro e provavelmente único."
    )
    required_permissions = frozenset({Permission.SCREEN_CAPTURE, Permission.GUI_CONTROL})
    agent_exposed = True
    parameters_schema = {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Texto do botão, link ou elemento visual."},
            "button": {"type": "string", "enum": ["left", "right", "middle"], "default": "left"},
            "match_index": {"type": "integer", "minimum": 0, "maximum": 4, "default": 0},
            "min_confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0, "default": 0.40},
        },
        "required": ["query"],
        "additionalProperties": False,
    }

    def __init__(self, bridge: NativeBridge | None = None, ocr: RapidOCREngine | None = None) -> None:
        self.bridge = bridge or NativeBridge()
        self.ocr = ocr or RapidOCREngine()

    def execute(
        self,
        context: ActionContext,
        *,
        query: str,
        button: str = "left",
        match_index: int = 0,
        min_confidence: float = 0.40,
        **kwargs: Any,
    ) -> ActionResult:
        del context, kwargs
        if not query.strip():
            raise ActionError("Informe um texto para localizar e clicar.")
        regions = self._read_regions(min_confidence)
        matches = self.ocr.find(regions, query, limit=5)
        index = int(match_index)
        if index < 0 or index >= len(matches):
            raise ActionError(
                f"Não há candidato de índice {index} para '{query}'. Candidatos encontrados: {len(matches)}."
            )
        target = matches[index]
        x, y = target.center
        try:
            self.bridge.move_cursor(x, y)
            self.bridge.click_mouse(button)
        except (NativeBackendUnavailableError, NativeOperationError) as exc:
            raise ActionError(str(exc)) from exc
        return ActionResult(
            True,
            self.name,
            f"Clique executado sobre o texto reconhecido '{target.text}'.",
            {
                "query": query,
                "matched_text": target.text,
                "confidence": target.confidence,
                "x": x,
                "y": y,
                "button": button,
            },
        )
