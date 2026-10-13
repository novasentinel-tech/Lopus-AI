"""Ativação e inspeção das features do Lopus."""

from nicegui import ui

from lopus.ui.context import get_ui_context
from lopus.ui.layout import app_layout
from lopus.ui.theme import apply_theme


@ui.page("/features")
def features_page() -> None:
    apply_theme()
    context = get_ui_context()
    manifests = context.features.discover()
    def set_enabled(feature_id: str, enabled: bool) -> None:
        values = set(context.settings.enabled_features)
        values.add(feature_id) if enabled else values.discard(feature_id)
        context.settings.enabled_features = sorted(values)
        context.save()
        ui.notify(f"Feature {'ativada' if enabled else 'desativada'}: {feature_id}", color="positive" if enabled else "warning")
    with app_layout("Features"):
        ui.label("Features").classes("text-3xl font-bold")
        ui.label("Capacidades internas do Lopus. Cada feature declara sua própria estrutura e as permissões que pode precisar.").classes("lopus-muted")
        if not manifests:
            ui.label("Nenhuma feature com manifest.json foi encontrada.").classes("text-amber-400")
        with ui.grid(columns=2).classes("w-full gap-4"):
            for feature in manifests:
                with ui.card().classes("lopus-card p-5"):
                    with ui.row().classes("w-full items-start"):
                        with ui.column().classes("gap-1"):
                            ui.label(feature.name).classes("text-xl font-bold")
                            ui.label(f"v{feature.version}").classes("lopus-muted text-xs")
                        ui.space()
                        ui.switch(value=feature.id in context.settings.enabled_features, on_change=lambda e, feature=feature: set_enabled(feature.id, bool(e.value)))
                    ui.label(feature.description).classes("lopus-muted text-sm")
                    ui.label("Permissões declaradas").classes("text-sm font-medium mt-2")
                    if feature.permissions:
                        for permission in feature.permissions:
                            ui.badge(permission).props("outline").classes("mr-1")
                    else:
                        ui.label("Nenhuma").classes("lopus-muted text-xs")
