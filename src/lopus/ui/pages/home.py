"""Página inicial do painel."""

from nicegui import ui

from lopus.ui.context import get_ui_context
from lopus.ui.layout import app_layout
from lopus.ui.theme import apply_theme


@ui.page("/home")
def home_page() -> None:
    apply_theme()
    context = get_ui_context()
    settings = context.settings
    with app_layout("Início"):
        ui.label("Visão geral").classes("text-3xl font-bold lopus-title")
        ui.label("Estado atual do agente, modelo e capacidades locais.").classes("lopus-muted")
        features = context.features.discover()
        plugins = context.plugins.discover()
        with ui.grid(columns=4).classes("w-full gap-4"):
            for title, value, detail, icon in (("Modelo", settings.model if settings.provider == "ollama" else "Demo", settings.provider, "memory"), ("Features", f"{len(settings.enabled_features)}/{len(features)}", "ativas", "extension"), ("Plugins", f"{len(settings.enabled_plugins)}/{len(plugins)}", "ativos", "power"), ("Permissões", str(len(settings.granted_permissions)), "concedidas", "verified_user")):
                with ui.card().classes("lopus-card p-5"):
                    ui.icon(icon).classes("text-blue-400 text-2xl")
                    ui.label(title).classes("lopus-muted text-sm")
                    ui.label(value).classes("text-2xl font-bold")
                    ui.label(detail).classes("lopus-muted text-xs")
        with ui.card().classes("lopus-card w-full p-6"):
            ui.label("Próximo passo").classes("text-xl font-bold")
            ui.label("Converse com o runtime atual ou configure quais capacidades o Lopus pode utilizar.").classes("lopus-muted")
            with ui.row().classes("gap-3 mt-2"):
                ui.button("Abrir Chat", icon="chat", on_click=lambda: ui.navigate.to("/chat"))
                ui.button("Gerenciar Features", icon="extension", on_click=lambda: ui.navigate.to("/features")).props("outline")
