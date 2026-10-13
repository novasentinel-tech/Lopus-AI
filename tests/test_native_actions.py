from __future__ import annotations

import unittest

from lopus.actions import (
    ActionContext,
    ClickAction,
    CursorPositionAction,
    HotkeyAction,
    MoveCursorAction,
    Permission,
    PermissionDeniedError,
    PermissionStore,
    PressKeyAction,
    TypeTextAction,
)


class FakeNativeBridge:
    def __init__(self) -> None:
        self.position = (12, 34)
        self.clicks: list[str] = []
        self.typed: list[str] = []
        self.keys: list[str] = []
        self.hotkeys: list[list[str]] = []

    def primary_screen_size(self) -> tuple[int, int]:
        return (1920, 1080)

    def cursor_position(self) -> tuple[int, int]:
        return self.position

    def move_cursor(self, x: int, y: int) -> None:
        self.position = (x, y)

    def click_mouse(self, button: str = "left") -> None:
        self.clicks.append(button)

    def type_text(self, text: str) -> None:
        self.typed.append(text)

    def press_key(self, key: str) -> None:
        self.keys.append(key)

    def hotkey(self, keys: list[str]) -> None:
        self.hotkeys.append(list(keys))


class NativeActionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.permissions = PermissionStore()
        self.context = ActionContext(permissions=self.permissions)
        self.bridge = FakeNativeBridge()

    def test_cursor_action_requires_gui_permission(self) -> None:
        action = CursorPositionAction(self.bridge)  # type: ignore[arg-type]
        with self.assertRaises(PermissionDeniedError):
            action.run(self.context)

    def test_cursor_actions_use_native_backend_after_permission(self) -> None:
        self.permissions.grant(Permission.GUI_CONTROL)
        move = MoveCursorAction(self.bridge)  # type: ignore[arg-type]
        read = CursorPositionAction(self.bridge)  # type: ignore[arg-type]

        result = move.run(self.context, x=120, y=240)
        self.assertTrue(result.success)
        self.assertEqual((120, 240), self.bridge.position)

        position = read.run(self.context)
        self.assertEqual(120, position.data["x"])
        self.assertEqual(240, position.data["y"])

    def test_click_moves_then_clicks(self) -> None:
        self.permissions.grant(Permission.GUI_CONTROL)
        action = ClickAction(self.bridge)  # type: ignore[arg-type]
        action.run(self.context, x=400, y=300, button="left")
        self.assertEqual((400, 300), self.bridge.position)
        self.assertEqual(["left"], self.bridge.clicks)

    def test_typing_has_independent_permission(self) -> None:
        action = TypeTextAction(self.bridge)  # type: ignore[arg-type]
        with self.assertRaises(PermissionDeniedError):
            action.run(self.context, text="Olá")
        self.permissions.grant(Permission.KEYBOARD_CONTROL)
        action.run(self.context, text="Olá")
        self.assertEqual(["Olá"], self.bridge.typed)

    def test_press_key_and_hotkey_use_keyboard_permission(self) -> None:
        press = PressKeyAction(self.bridge)  # type: ignore[arg-type]
        hotkey = HotkeyAction(self.bridge)  # type: ignore[arg-type]
        with self.assertRaises(PermissionDeniedError):
            press.run(self.context, key="enter")

        self.permissions.grant(Permission.KEYBOARD_CONTROL)
        press.run(self.context, key="enter")
        hotkey.run(self.context, keys=["ctrl", "l"])
        self.assertEqual(["enter"], self.bridge.keys)
        self.assertEqual([["ctrl", "l"]], self.bridge.hotkeys)


if __name__ == "__main__":
    unittest.main()
