import unittest

from lopus.ui.environment import UIEnvironment


class UIEnvironmentTests(unittest.TestCase):
    def test_codespaces_uses_web_mode(self) -> None:
        config = UIEnvironment.launch_config({"CODESPACES": "true"})
        self.assertEqual(config.mode, "codespaces")
        self.assertFalse(config.native)
        self.assertEqual(config.host, "0.0.0.0")
        self.assertEqual(config.port, 8080)
        self.assertFalse(config.show_browser)

    def test_forwarding_domain_also_detects_codespaces(self) -> None:
        config = UIEnvironment.launch_config(
            {"GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN": "app.github.dev"}
        )
        self.assertEqual(config.mode, "codespaces")
        self.assertFalse(config.native)

    def test_local_environment_uses_native_mode(self) -> None:
        config = UIEnvironment.launch_config({})
        self.assertEqual(config.mode, "local")
        self.assertTrue(config.native)
        self.assertEqual(config.host, "127.0.0.1")

    def test_port_can_be_overridden(self) -> None:
        config = UIEnvironment.launch_config(
            {"CODESPACES": "true", "LOPUS_UI_PORT": "9000"}
        )
        self.assertEqual(config.port, 9000)

    def test_invalid_port_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            UIEnvironment.launch_config({"LOPUS_UI_PORT": "abc"})


if __name__ == "__main__":
    unittest.main()
