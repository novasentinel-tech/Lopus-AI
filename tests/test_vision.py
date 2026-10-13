from __future__ import annotations

import unittest

from lopus.actions import ActionContext, ClickTextAction, Permission, PermissionDeniedError, PermissionStore
from lopus.vision import OCRRegion, RapidOCREngine


class FakeNativeBridge:
    def __init__(self) -> None:
        self.position = (0, 0)
        self.clicks: list[str] = []

    def capture_primary_screen_bmp(self) -> bytes:
        return b"fake-bmp"

    def move_cursor(self, x: int, y: int) -> None:
        self.position = (x, y)

    def click_mouse(self, button: str = "left") -> None:
        self.clicks.append(button)


class FakeOCR:
    def recognize(self, encoded_image: bytes, *, min_confidence: float = 0.35):
        self.last_image = encoded_image
        self.last_confidence = min_confidence
        return (
            OCRRegion(
                text="Configurações",
                confidence=0.96,
                box=((100, 200), (220, 200), (220, 240), (100, 240)),
            ),
            OCRRegion(
                text="Cancelar",
                confidence=0.91,
                box=((300, 400), (380, 400), (380, 430), (300, 430)),
            ),
        )

    def find(self, regions, query: str, *, limit: int = 5):
        return RapidOCREngine.find(regions, query, limit=limit)


class VisionTests(unittest.TestCase):
    def test_ocr_region_center(self) -> None:
        region = OCRRegion(
            text="Salvar",
            confidence=0.9,
            box=((10, 20), (110, 20), (110, 60), (10, 60)),
        )
        self.assertEqual(region.center, (60, 40))

    def test_find_prefers_text_match(self) -> None:
        regions = (
            OCRRegion("Configurações", 0.95, ((0, 0), (10, 0), (10, 10), (0, 10))),
            OCRRegion("Conta", 0.99, ((20, 0), (30, 0), (30, 10), (20, 10))),
        )
        result = RapidOCREngine.find(regions, "configuracoes", limit=5)
        # Sem normalização de acentos, a busca fuzzy ainda deve localizar a palavra correta.
        self.assertTrue(result)
        self.assertEqual(result[0].text, "Configurações")

    def test_click_text_requires_both_permissions(self) -> None:
        permissions = PermissionStore()
        context = ActionContext(permissions=permissions)
        action = ClickTextAction(FakeNativeBridge(), FakeOCR())  # type: ignore[arg-type]

        permissions.grant(Permission.SCREEN_CAPTURE)
        with self.assertRaises(PermissionDeniedError):
            action.run(context, query="Configurações")

    def test_click_text_moves_to_ocr_center_and_clicks(self) -> None:
        permissions = PermissionStore((Permission.SCREEN_CAPTURE, Permission.GUI_CONTROL))
        context = ActionContext(permissions=permissions)
        bridge = FakeNativeBridge()
        action = ClickTextAction(bridge, FakeOCR())  # type: ignore[arg-type]

        result = action.run(context, query="Configurações")
        self.assertTrue(result.success)
        self.assertEqual(bridge.position, (160, 220))
        self.assertEqual(bridge.clicks, ["left"])
        self.assertEqual(result.data["matched_text"], "Configurações")


if __name__ == "__main__":
    unittest.main()
