"""Chat local conectado ao runtime atual."""

import asyncio

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
        ui.label(f"Provider: {context.settings.provider} · Modelo: {context.settings.model}").classes("lopus-muted")
        messages = ui.column().classes("w-full gap-2")
        with messages:
            ui.chat_message("Runtime iniciado. Nesta versão eu respondo pelo modelo configurado e respeito as permissões persistidas do painel.", name="Lopus")
        with ui.row().classes("w-full items-end gap-2"):
            prompt = ui.textarea(placeholder="Digite uma mensagem para o Lopus...").props("autogrow outlined").classes("flex-grow")
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
            ui.button(icon="send", on_click=send).props("round")
