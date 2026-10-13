"""Inicialização do painel local do Lopus-AI."""

from nicegui import ui

from lopus.ui.context import get_ui_context
from lopus.ui.environment import UIEnvironment
from lopus.ui.pages import chat, features, home, models, plugins, setup  # noqa: F401


@ui.page("/")
def root_page() -> None:
    context = get_ui_context()
    ui.navigate.to("/home" if context.settings.setup_complete else "/setup")


def main() -> None:
    launch = UIEnvironment.launch_config()

    if launch.mode == "codespaces":
        print(
            f"Lopus-AI: painel em modo Codespaces na porta {launch.port}. "
            "Abra a porta encaminhada pelo GitHub no navegador."
        )
        ui.run(
            title="Lopus-AI",
            favicon="🧠",
            native=False,
            host=launch.host,
            port=launch.port,
            show=launch.show_browser,
            reload=False,
            dark=True,
            language="pt-BR",
        )
        return

    ui.run(
        title="Lopus-AI",
        favicon="🧠",
        native=True,
        reload=False,
        dark=True,
        language="pt-BR",
        window_size=(1280, 820),
    )
