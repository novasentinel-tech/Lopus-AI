"""Inicialização do painel desktop local do Lopus-AI."""

from nicegui import ui

from lopus.ui.context import get_ui_context
from lopus.ui.pages import chat, features, home, models, plugins, setup  # noqa: F401


@ui.page("/")
def root_page() -> None:
    context = get_ui_context()
    ui.navigate.to("/home" if context.settings.setup_complete else "/setup")


def main() -> None:
    ui.run(title="Lopus-AI", favicon="🧠", native=True, reload=False, dark=True, language="pt-BR", window_size=(1280, 820))
