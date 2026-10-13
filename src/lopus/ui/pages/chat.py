"""Chat local conectado ao runtime atual."""

import asyncio
import json

from nicegui import ui

from lopus.models.base import ModelError
from lopus.ui.context import get_ui_context
from lopus.ui.layout import app_layout
from lopus.ui.runtime import runtime_from_settings
from lopus.ui.theme import apply_theme


@ui.page("/chat")
def chat_page() -> None:
    apply_theme()
    context = get_ui_context()
    runtime = runtime_from_settings(context.settings)
    with app_layout("Chat"):
        ui.label("Chat local").classes("text-3xl font-bold")
        ui.label(
            f"Provider: {context.settings.provider} · Modelo: {context.settings.model}"
        ).classes("lopus-muted")
        ui.label(
            "Quando o modelo solicitar uma Action, a execução aparece abaixo da resposta."
        ).classes("lopus-muted text-sm")

        messages = ui.column().classes("w-full gap-2")
        with messages:
            ui.chat_message(
                "Runtime iniciado. Posso usar apenas Actions expostas e permissões concedidas no painel.",
                name="Lopus",
            )

        with ui.row().classes("w-full items-end gap-2"):
            prompt = ui.textarea(placeholder="Digite uma mensagem para o Lopus...").props(
                "autogrow outlined"
            ).classes("flex-grow")

            async def send() -> None:
                text = (prompt.value or "").strip()
                if not text:
                    return
                prompt.value = ""
                with messages:
                    ui.chat_message(text, name="Você", sent=True)
                    with ui.chat_message(name="Lopus"):
                        answer_label = ui.label("Pensando...").classes("whitespace-pre-wrap")
                try:
                    answer = await asyncio.to_thread(runtime.reply, text)
                except (ModelError, ValueError) as exc:
                    answer = f"Erro: {exc}"
                answer_label.set_text(answer)

                trace = runtime.last_agent_trace
                if trace:
                    with messages:
                        with ui.expansion(
                            f"Ações do agente ({len(trace)})",
                            icon="account_tree",
                        ).classes("w-full lopus-card"):
                            for step in trace:
                                status = "✓" if step.success else "✕"
                                ui.label(
                                    f"{status} ciclo {step.iteration} · {step.action_name or step.tool_name}"
                                ).classes("font-semibold")
                                ui.label(step.message).classes("lopus-muted text-sm")
                                if step.arguments:
                                    ui.code(
                                        json.dumps(step.arguments, ensure_ascii=False, indent=2, default=str),
                                        language="json",
                                    ).classes("w-full")

            ui.button(icon="send", on_click=send).props("round")
