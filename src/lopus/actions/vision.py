"""Actions de percepção visual: captura de tela e OCR local."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from lopus.actions.base import Action, ActionContext, ActionError, ActionResult, Permission
from lopus.native import NativeBackendUnavailableError, NativeBridge, NativeOperationError
from lopus.vision import OCRUnavailableError, RapidOCREngine


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


class ReadScreenAction(Action):
    name = "vision.read_screen"
    description = (
        "Observa a tela atual com OCR local e retorna textos visíveis, confiança e coordenadas. "
        "Use esta ação antes de clicar quando não souber onde está o elemento."
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

    def execute(
        self,
        context: ActionContext,
        *,
        min_confidence: float = 0.45,
        max_regions: int = 120,
        **kwargs: Any,
    ) -> ActionResult:
        del context, kwargs
        try:
            bmp = self.bridge.capture_primary_screen_bmp()
            width, height = self.bridge.primary_screen_size()
            regions = self.ocr.recognize(bmp, min_confidence=float(min_confidence))
        except (NativeBackendUnavailableError, NativeOperationError, OCRUnavailableError) as exc:
            raise ActionError(str(exc)) from exc

        limited = regions[: max(1, min(int(max_regions), 200))]
        lines = [region.text for region in limited]
        return ActionResult(
            True,
            self.name,
            f"Tela observada: {len(limited)} regiões de texto reconhecidas.",
            {
                "screen": {"width": width, "height": height},
                "text": "\n".join(lines),
                "regions": [region.as_dict() for region in limited],
                "truncated": len(regions) > len(limited),
            },
        )


class FindTextOnScreenAction(Action):
    name = "vision.find_text"
    description = (
        "Procura um texto na tela atual usando OCR e devolve candidatos com coordenadas centrais. "
        "Use o centro retornado em gui.click ou gui.move_cursor."
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

    def execute(
        self,
        context: ActionContext,
        *,
        query: str,
        limit: int = 5,
        min_confidence: float = 0.35,
        **kwargs: Any,
    ) -> ActionResult:
        del context, kwargs
        if not query.strip():
            raise ActionError("Informe um texto para procurar na tela.")
        try:
            bmp = self.bridge.capture_primary_screen_bmp()
            regions = self.ocr.recognize(bmp, min_confidence=float(min_confidence))
            matches = self.ocr.find(regions, query, limit=max(1, min(int(limit), 10)))
        except (NativeBackendUnavailableError, NativeOperationError, OCRUnavailableError) as exc:
            raise ActionError(str(exc)) from exc

        return ActionResult(
            True,
            self.name,
            f"Busca visual concluída: {len(matches)} candidato(s) para '{query}'.",
            {
                "query": query,
                "matches": [region.as_dict() for region in matches],
            },
        )
