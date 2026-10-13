import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from lopus.features import FeatureManager


class FeatureManagerTests(unittest.TestCase):
    def test_discovers_manifests(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            feature = root / "documents"
            feature.mkdir()
            (feature / "manifest.json").write_text(json.dumps({"id": "documents", "name": "Documentos", "description": "Teste", "version": "1.0.0", "permissions": ["file.read"]}), encoding="utf-8")
            manifests = FeatureManager(root).discover()
            self.assertEqual(len(manifests), 1)
            self.assertEqual(manifests[0].id, "documents")
            self.assertEqual(manifests[0].permissions, ("file.read",))


if __name__ == "__main__":
    unittest.main()
