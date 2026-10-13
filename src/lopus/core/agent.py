"""Loop de execução do agente principal com tool calling controlado."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from lopus.actions import ActionContext, ActionError, ActionRegistry, PermissionDeniedError, PermissionStore
from lopus.models.base import ModelError, ModelProvider


@dataclass(frozen=True, slots=True)
class AgentTraceStep:
    iteration: int
    tool_name: str
    action_name: str | None
    arguments: Mapping[str, Any]
    success: bool
    message: str
    data: Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class AgentRunResult:
    content: str
    trace: tuple[AgentTraceStep, ...]
    iterations: int


class AgentLoopError(ModelError):
    """O agente excedeu seus limites de segurança/execução."""


class AgentExecutor:
    """Conecta decisões estruturadas do modelo às Actions reais do runtime."""

    def __init__(
        self,
        *,
        model: ModelProvider,
        actions: ActionRegistry,
        permissions: PermissionStore,
        max_iterations: int = 8,
        max_tool_calls: int = 20,
        repeat_limit: int = 2,
    ) -> None:
        self.model = model
        self.actions = actions
        self.permissions = permissions
        self.max_iterations = max_iterations
        self.max_tool_calls = max_tool_calls
        self.repeat_limit = repeat_limit

    @staticmethod
    def _json_safe(value: Any) -> Any:
        try:
            json.dumps(value, ensure_ascii=False)
            return value
        except TypeError:
            return str(value)

    def run(self, messages: Sequence[Mapping[str, Any]]) -> AgentRunResult:
        conversation: list[dict[str, Any]] = [dict(message) for message in messages]
        tools = self.actions.agent_tool_schemas()
        trace: list[AgentTraceStep] = []
        call_count = 0
        repeated: dict[str, int] = {}

        for iteration in range(1, self.max_iterations + 1):
            turn = self.model.generate_with_tools(conversation, tools)
            assistant_message = dict(turn.assistant_message) or {
                "role": "assistant",
                "content": turn.content,
            }
            conversation.append(assistant_message)

            if not turn.tool_calls:
                content = turn.content.strip()
                if not content:
                    content = "A tarefa foi processada, mas o modelo não retornou uma resposta textual."
                return AgentRunResult(content=content, trace=tuple(trace), iterations=iteration)

            for call in turn.tool_calls:
                call_count += 1
                if call_count > self.max_tool_calls:
                    raise AgentLoopError(
                        f"O agente excedeu o limite de {self.max_tool_calls} ações em uma única tarefa."
                    )

                arguments = dict(call.arguments)
                fingerprint = f"{call.name}:{json.dumps(arguments, sort_keys=True, ensure_ascii=False, default=str)}"
                repeated[fingerprint] = repeated.get(fingerprint, 0) + 1

                if repeated[fingerprint] > self.repeat_limit:
                    payload = {
                        "success": False,
                        "error": "repeated_action",
                        "message": "A mesma ação com os mesmos argumentos foi bloqueada por repetição.",
                    }
                    conversation.append(
                        {
                            "role": "tool",
                            "tool_name": call.name,
                            "content": json.dumps(payload, ensure_ascii=False),
                        }
                    )
                    trace.append(
                        AgentTraceStep(
                            iteration=iteration,
                            tool_name=call.name,
                            action_name=None,
                            arguments=arguments,
                            success=False,
                            message=payload["message"],
                            data={},
                        )
                    )
                    continue

                action_name: str | None = None
                try:
                    action = self.actions.get_by_tool_name(call.name)
                    action_name = action.name
                    result = action.run(
                        ActionContext(
                            permissions=self.permissions,
                            actor="agent",
                            metadata={"iteration": iteration},
                        ),
                        **arguments,
                    )
                    payload = {
                        "success": result.success,
                        "action": result.action,
                        "message": result.message,
                        "data": self._json_safe(dict(result.data)),
                    }
                    success = result.success
                    message = result.message
                    result_data = dict(result.data)
                except PermissionDeniedError as exc:
                    result_data = {
                        "error": "permission_denied",
                        "missing_permissions": list(exc.missing_permissions),
                    }
                    payload = {
                        "success": False,
                        "error": "permission_denied",
                        "message": str(exc),
                        "missing_permissions": list(exc.missing_permissions),
                    }
                    success = False
                    message = str(exc)
                except (ActionError, KeyError, PermissionError, TypeError, ValueError) as exc:
                    payload = {
                        "success": False,
                        "error": type(exc).__name__,
                        "message": str(exc),
                    }
                    success = False
                    message = str(exc)
                    result_data = {"error": type(exc).__name__}
                except Exception as exc:  # barreira para não derrubar o loop inteiro
                    payload = {
                        "success": False,
                        "error": "action_internal_error",
                        "message": f"Falha interna na ação: {exc}",
                    }
                    success = False
                    message = payload["message"]
                    result_data = {"error": "action_internal_error"}

                conversation.append(
                    {
                        "role": "tool",
                        "tool_name": call.name,
                        "content": json.dumps(payload, ensure_ascii=False, default=str),
                    }
                )
                trace.append(
                    AgentTraceStep(
                        iteration=iteration,
                        tool_name=call.name,
                        action_name=action_name,
                        arguments=arguments,
                        success=success,
                        message=message,
                        data=result_data,
                    )
                )

        raise AgentLoopError(
            f"O agente excedeu o limite de {self.max_iterations} ciclos de decisão."
        )
