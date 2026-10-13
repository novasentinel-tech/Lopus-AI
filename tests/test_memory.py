import unittest

from lopus.memory.session import SessionMemory


class SessionMemoryTests(unittest.TestCase):
    def test_keeps_only_the_configured_limit(self) -> None:
        memory = SessionMemory(max_messages=2)
        memory.add("user", "um")
        memory.add("assistant", "dois")
        memory.add("user", "tres")

        self.assertEqual([m.content for m in memory.snapshot()], ["dois", "tres"])

    def test_clear_removes_all_messages(self) -> None:
        memory = SessionMemory()
        memory.add("user", "teste")
        memory.clear()
        self.assertEqual(len(memory), 0)


if __name__ == "__main__":
    unittest.main()
