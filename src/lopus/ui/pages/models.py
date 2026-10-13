"""Gerenciamento de modelos locais."""

from nicegui import ui

from lopus.models.catalog import MODEL_CATALOG
from lopus.models.manager import OllamaUnavailableError
from lopus.ui.context import get_ui_context
from lopus.ui.layout import app_layout
from lopus.ui.theme import apply_theme


@ui.page("/models")
def models_page() -> None:
    apply_theme()
    context = get_ui_context()
    with app_layout("Modelos"):
        ui.label("Modelos locais").classes("text-3xl font-bold")
        ui.label("Baixe, visualize e escolha o modelo utilizado pelo runtime.").classes("lopus-muted")
        status = ui.label("").classes("lopus-muted")
        @ui.refreshable
        def installed_section() -> None:
            with ui.card().classes("lopus-card w-full p-5"):
                ui.label("Instalados").classes("text-xl font-bold")
                if not context.ollama.is_running():
                    ui.label("A API local do Ollama não está disponível.").classes("text-amber-400")
                    return
                try:
                    installed = context.ollama.list_installed()
                except OllamaUnavailableError as exc:
                    ui.label(str(exc)).classes("text-red-400")
                    return
                if not installed:
                    ui.label("Nenhum modelo instalado.").classes("lopus-muted")
                for model in installed:
                    with ui.row().classes("w-full items-center py-2"):
                        ui.label(model.name).classes("font-medium")
                        ui.label(f"{model.size_gb:.1f} GB").classes("lopus-muted text-sm")
                        ui.space()
                        active = context.settings.provider == "ollama" and context.settings.model == model.name
                        if active:
                            ui.badge("ATIVO", color="positive")
                        else:
                            ui.button("Usar", on_click=lambda model=model: activate(model.name)).props("outline dense")
        def activate(model_name: str) -> None:
            context.settings.provider = "ollama"
            context.settings.model = model_name
            context.settings.setup_complete = True
            context.save()
            ui.notify(f"Modelo ativo: {model_name}", color="positive")
            installed_section.refresh()
        async def download(model_id: str) -> None:
            status.set_text(f"Baixando {model_id}...")
            try:
                await context.ollama.pull(model_id, on_status=lambda line: status.set_text(line[-120:]))
            except (OllamaUnavailableError, RuntimeError) as exc:
                ui.notify(str(exc), color="negative")
                return
            ui.notify(f"{model_id} baixado.", color="positive")
            status.set_text("")
            installed_section.refresh()
        installed_section()
        ui.label("Catálogo sugerido").classes("text-2xl font-bold mt-4")
        with ui.grid(columns=3).classes("w-full gap-4"):
            for option in MODEL_CATALOG:
                with ui.card().classes("lopus-card p-5"):
                    ui.label(option.name).classes("text-lg font-bold")
                    ui.label(option.size).classes("text-blue-300")
                    ui.label(option.description).classes("lopus-muted text-sm")
                    ui.button("Baixar", icon="download", on_click=lambda option=option: download(option.id)).classes("mt-2")
