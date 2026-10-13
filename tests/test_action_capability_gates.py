from __future__ import annotations

import unittest

from lopus.actions import create_default_action_registry


class ActionCapabilityGateTests(unittest.TestCase):
    def test_panel_with_nothing_enabled_hides_optional_native_tools(self) -> None:
        registry = create_default_action_registry(enabled_features=[], enabled_plugins=[])
        names = registry.names()
        self.assertNotIn("vision.read_screen", names)
        self.assertNotIn("vision.find_text", names)
        self.assertNotIn("vision.click_text", names)
        self.assertNotIn("gui.click", names)
        self.assertNotIn("gui.type_text", names)
        self.assertIn("system.native_info", names)

    def test_screen_feature_requires_screen_capture_plugin(self) -> None:
        without_plugin = create_default_action_registry(
            enabled_features=["screen_perception"],
            enabled_plugins=[],
        )
        self.assertNotIn("vision.read_screen", without_plugin.names())

        with_plugin = create_default_action_registry(
            enabled_features=["screen_perception"],
            enabled_plugins=["screen_capture"],
        )
        self.assertIn("vision.read_screen", with_plugin.names())
        self.assertIn("vision.find_text", with_plugin.names())
        self.assertNotIn("vision.click_text", with_plugin.names())

    def test_click_text_requires_mouse_plugin_to_be_registered(self) -> None:
        registry = create_default_action_registry(
            enabled_features=["screen_perception"],
            enabled_plugins=["screen_capture", "mouse_pointer"],
        )
        self.assertIn("vision.click_text", registry.names())
        self.assertIn("gui.click", registry.names())

    def test_keyboard_plugin_registers_typing_tool(self) -> None:
        registry = create_default_action_registry(
            enabled_features=[],
            enabled_plugins=["keyboard_input"],
        )
        self.assertIn("gui.type_text", registry.names())


if __name__ == "__main__":
    unittest.main()
