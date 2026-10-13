from __future__ import annotations

import unittest

from lopus.actions import (
    ActionContext,
    CursorPositionAction,
    MoveCursorAction,
    Permission,
    PermissionDeniedError,
    PermissionStore,
)


class FakeNativeBridge:
    def __init__(self) -> None:
        self.position = (12, 34)

    def cursor_position(self) -> tuple[int, int]:
        return self.position

    def move_cursor(self, x: int, y: int) -> None:
        self.position = (x, y)


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


if __name__ == "__main__":
    unittest.main()
