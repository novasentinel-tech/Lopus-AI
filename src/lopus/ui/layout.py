"""Layout compartilhado pelas páginas principais do painel."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from nicegui import ui

NAV_ITEMS = (("Início", "/home", "home"), ("Chat", "/chat", "chat"), ("Modelos", "/models", "memory"), ("Features", "/features", "extension"), ("Plugins", "/plugins", "power"))


@contextmanager
def app_layout(title: str) -> Iterator[None]:
    with ui.header().classes("items-center bg-slate-950 border-b border-slate-800"):
        ui.label("LOPUS").classes("font-black text-xl tracking-widest")
        ui.label(title).classes("lopus-muted text-sm")
        ui.space()
        ui.badge("LOCAL", color="positive").props("outline")
    with ui.left_drawer(value=True).classes("bg-slate-950 border-r border-slate-800"):
        ui.label("Lopus-AI").classes("text-2xl font-bold lopus-title mb-4")
        ui.label("Painel local").classes("lopus-muted text-xs mb-6")
        for label, route, icon in NAV_ITEMS:
            ui.button(label, icon=icon, on_click=lambda route=route: ui.navigate.to(route)).props("flat align=left").classes("w-full justify-start mb-1")
        ui.separator().classes("my-4")
        ui.button("Configuração inicial", icon="settings", on_click=lambda: ui.navigate.to("/setup")).props("flat align=left").classes("w-full justify-start")
    with ui.column().classes("w-full max-w-6xl mx-auto p-6 gap-5"):
        yield
