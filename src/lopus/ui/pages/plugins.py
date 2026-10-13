"""Plugins externos e permissões persistentes."""

from nicegui import ui

from lopus.actions import Permission
from lopus.ui.context import get_ui_context
from lopus.ui.layout import app_layout
from lopus.ui.theme import apply_theme


@ui.page("/plugins")
def plugins_page() -> None:
    apply_theme()
    context = get_ui_context()
    plugins = context.plugins.discover()
    def set_plugin(plugin_id: str, enabled: bool) -> None:
        values = set(context.settings.enabled_plugins)
        values.add(plugin_id) if enabled else values.discard(plugin_id)
        context.settings.enabled_plugins = sorted(values)
        context.save()
    def set_permission(permission: str, enabled: bool) -> None:
        values = set(context.settings.granted_permissions)
        values.add(permission) if enabled else values.discard(permission)
        context.settings.granted_permissions = sorted(values)
        context.save()
    with app_layout("Plugins e permissões"):
        ui.label("Plugins").classes("text-3xl font-bold")
        ui.label("Integrações externas ficam separadas das features e não recebem permissões automaticamente.").classes("lopus-muted")
        with ui.grid(columns=2).classes("w-full gap-4"):
            for plugin in plugins:
                with ui.card().classes("lopus-card p-5"):
                    with ui.row().classes("w-full items-start"):
                        with ui.column().classes("gap-1"):
                            ui.label(plugin.name).classes("text-xl font-bold")
                            ui.label(f"v{plugin.version}").classes("lopus-muted text-xs")
                        ui.space()
                        ui.switch(value=plugin.id in context.settings.enabled_plugins, on_change=lambda e, plugin=plugin: set_plugin(plugin.id, bool(e.value)))
                    ui.label(plugin.description).classes("lopus-muted text-sm")
                    if plugin.permissions:
                        ui.label("Pode solicitar:").classes("text-sm mt-2")
                        for permission in plugin.permissions:
                            ui.badge(permission).props("outline").classes("mr-1")
        ui.separator().classes("my-4")
        ui.label("Permissões do runtime").classes("text-2xl font-bold")
        ui.label("Essas concessões são persistidas localmente e aplicadas ao runtime do Chat.").classes("lopus-muted")
        with ui.card().classes("lopus-card w-full p-5"):
            for permission in Permission:
                with ui.row().classes("w-full items-center"):
                    ui.label(permission.value).classes("font-medium")
                    ui.space()
                    ui.switch(value=permission.value in context.settings.granted_permissions, on_change=lambda e, permission=permission: set_permission(permission.value, bool(e.value)))
