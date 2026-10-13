from __future__ import annotations

import unittest
from collections.abc import Sequence
from typing import Any, Mapping

from lopus.actions import Action, ActionContext, ActionRegistry, ActionResult, Permission, PermissionStore
from lopus.core.agent import AgentExecutor
from lopus.core.types import Message
from lopus.models.base import ModelProvider
from lopus.models.tools import ModelTurn, ToolCall


class ScriptedProvider(ModelProvider):
    name = "scripted"

    def __init__(self, turns: list[ModelTurn]) -> None:
        self.turns = list(turns)
        self.seen_messages: list[list[Mapping[str, Any]]] = []
        self.seen_tools: list[list[Mapping[str, Any]]] = []

    def generate(self, messages: Sequence[Message]) -> str:
        return "fallback"

    def generate_with_tools(self, messages, tools):  # type: ignore[override]
        self.seen_messages.append(list(messages))
        self.seen_tools.append(list(tools))
        return self.turns.pop(0)


class EchoAction(Action):
    name = "test.echo"
    description = "Repete um texto."
    agent_exposed = True
    parameters_schema = {
        "type": "object",
        "properties": {"text": {"type": "string"}},
        "required": ["text"],
        "additionalProperties": False,
    }

    def execute(self, context: ActionContext, *, text: str) -> ActionResult:
        return ActionResult(True, self.name, "ok", {"echo": text})


class ProtectedAction(EchoAction):
    name = "test.protected"
    required_permissions = frozenset({Permission.GUI_CONTROL})


class AgentActionLoopTests(unittest.TestCase):
    def test_model_can_call_registered_action_and_receive_observation(self) -> None:
        registry = ActionRegistry()
        action = EchoAction()
        registry.register(action)
        provider = ScriptedProvider(
            [
                ModelTurn(
                    content="",
                    tool_calls=(ToolCall(action.tool_name, {"text": "oi"}),),
                    assistant_message={
                        "role": "assistant",
                        "content": "",
                        "tool_calls": [
                            {
                                "type": "function",
                                "function": {"name": action.tool_name, "arguments": {"text": "oi"}},
                            }
                        ],
                    },
                ),
                ModelTurn(
                    content="Concluído.",
                    assistant_message={"role": "assistant", "content": "Concluído."},
                ),
            ]
        )
        executor = AgentExecutor(model=provider, actions=registry, permissions=PermissionStore())
        result = executor.run([{"role": "user", "content": "repita oi"}])

        self.assertEqual(result.content, "Concluído.")
        self.assertEqual(len(result.trace), 1)
        self.assertTrue(result.trace[0].success)
        self.assertEqual(result.trace[0].data["echo"], "oi")
        tool_messages = [m for m in provider.seen_messages[1] if m.get("role") == "tool"]
        self.assertEqual(len(tool_messages), 1)
        self.assertIn('"echo": "oi"', str(tool_messages[0]["content"]))

    def test_permission_denial_is_returned_to_model_instead_of_executing(self) -> None:
        registry = ActionRegistry()
        action = ProtectedAction()
        registry.register(action)
        provider = ScriptedProvider(
            [
                ModelTurn(
                    content="",
                    tool_calls=(ToolCall(action.tool_name, {"text": "bloqueado"}),),
                    assistant_message={"role": "assistant", "content": "", "tool_calls": []},
                ),
                ModelTurn(
                    content="Preciso da permissão gui.control.",
                    assistant_message={"role": "assistant", "content": "Preciso da permissão gui.control."},
                ),
            ]
        )
        executor = AgentExecutor(model=provider, actions=registry, permissions=PermissionStore())
        result = executor.run([{"role": "user", "content": "execute"}])

        self.assertFalse(result.trace[0].success)
        self.assertIn("gui.control", result.trace[0].message)
        self.assertIn("gui.control", result.content)

    def test_hidden_action_is_not_sent_as_tool(self) -> None:
        class HiddenAction(EchoAction):
            name = "test.hidden"
            agent_exposed = False

        registry = ActionRegistry()
        registry.register(HiddenAction())
        self.assertEqual(registry.agent_tool_schemas(), ())


if __name__ == "__main__":
    unittest.main()
