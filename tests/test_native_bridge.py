from __future__ import annotations

import unittest

from lopus.native import NativeBridge


class NativeBridgeTests(unittest.TestCase):
    def test_capabilities_are_safe_even_if_extension_is_missing(self) -> None:
        capabilities = NativeBridge().capabilities()
        self.assertIsInstance(capabilities.available, bool)
        self.assertIsInstance(capabilities.platform, str)

    def test_compiled_backend_reports_process_when_available(self) -> None:
        bridge = NativeBridge()
        if not bridge.available:
            self.skipTest("Extensão C++ não foi compilada neste ambiente")
        capabilities = bridge.capabilities()
        self.assertTrue(capabilities.available)
        self.assertIsInstance(capabilities.process_id, int)
        self.assertGreater(capabilities.process_id or 0, 0)
        self.assertIn(capabilities.platform, {"windows", "linux", "macos", "unknown"})


if __name__ == "__main__":
    unittest.main()
