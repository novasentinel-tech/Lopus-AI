from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from lopus.actions import (
    ActionContext,
    Permission,
    PermissionDeniedError,
    PermissionStore,
    create_default_action_registry,
)


class ActionTests(unittest.TestCase):
    def test_action_is_blocked_without_permission(self) -> None:
        registry = create_default_action_registry()
        context = ActionContext(permissions=PermissionStore())

        with self.assertRaises(PermissionDeniedError):
            registry.execute("file.inspect", context, path=".")

    def test_write_read_and_inspect_text_file(self) -> None:
        registry = create_default_action_registry()
        permissions = PermissionStore(
            (Permission.FILE_READ, Permission.FILE_WRITE)
        )
        context = ActionContext(permissions=permissions)

        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "teste.txt"
            write_result = registry.execute(
                "file.write_text",
                context,
                path=str(path),
                content="Lopus",
            )
            self.assertTrue(write_result.success)

            read_result = registry.execute(
                "file.read_text",
                context,
                path=str(path),
            )
            self.assertEqual(read_result.data["content"], "Lopus")

            inspect_result = registry.execute(
                "file.inspect",
                context,
                path=str(path),
            )
            self.assertTrue(inspect_result.data["is_file"])


if __name__ == "__main__":
    unittest.main()
