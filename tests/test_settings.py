from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from lopus.settings import AppSettings, SettingsStore


class SettingsStoreTests(unittest.TestCase):
    def test_roundtrip(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            store = SettingsStore(path)
            settings = AppSettings(setup_complete=True, provider="ollama", model="qwen3:4b", enabled_features=["documents"], granted_permissions=["file.read"])
            store.save(settings)
            loaded = store.load()
            self.assertTrue(loaded.setup_complete)
            self.assertEqual(loaded.provider, "ollama")
            self.assertEqual(loaded.model, "qwen3:4b")
            self.assertEqual(loaded.enabled_features, ["documents"])
            self.assertEqual(loaded.granted_permissions, ["file.read"])


if __name__ == "__main__":
    unittest.main()
