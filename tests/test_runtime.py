import unittest

from lopus.core.runtime import LopusRuntime
from lopus.memory.session import SessionMemory
from lopus.models.demo import DemoProvider


class RuntimeTests(unittest.TestCase):
    def test_demo_flow_is_end_to_end(self) -> None:
        runtime = LopusRuntime(DemoProvider(), SessionMemory(max_messages=4))
        answer = runtime.reply("Olá, Lopus")

        self.assertIn("Modo demo ativo", answer)
        self.assertEqual(runtime.status()["messages_in_memory"], 2)


if __name__ == "__main__":
    unittest.main()
