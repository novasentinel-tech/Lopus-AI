"""Assistente de configuração inicial."""

from nicegui import ui

from lopus.models.catalog import MODEL_CATALOG
from lopus.models.manager import OllamaUnavailableError
from lopus.ui.context import get_ui_context
from lopus.ui.theme import apply_theme


@ui.page("/setup")
def setup_page() -> None:
    apply_theme()
    context = get_ui_context()
    selected = {"model": context.settings.model}
    with ui.column().classes("w-full max-w-5xl mx-auto p-8 gap-6"):
        ui.label("LOPUS").classes("text-3xl font-black tracking-widest text-blue-400")
        ui.label("Configuração inicial").classes("text-4xl font-bold lopus-title")
        ui.label("Escolha como o Lopus deve começar. Tudo desta interface roda localmente.").classes("lopus-muted text-lg")
        installed = context.ollama.is_installed()
        running = context.ollama.is_running()
        with ui.card().classes("lopus-card w-full p-5"):
            ui.label("Runtime local").classes("font-semibold text-lg")
            if installed and running:
                ui.label("Ollama detectado e em execução.").classes("text-green-400")
            elif installed:
                ui.label("Ollama está instalado, mas a API local não respondeu. Abra o Ollama antes de baixar ou usar modelos.").classes("text-amber-400")
            else:
                ui.label("Ollama ainda não foi encontrado. Instale-o para usar modelos locais.").classes("text-amber-400")
        selection_label = ui.label(f"Selecionado: {selected['model']}").classes("text-blue-300 font-medium")
        def select_model(model_id: str) -> None:
            selected["model"] = model_id
            selection_label.set_text(f"Selecionado: {model_id}")
        with ui.grid(columns=3).classes("w-full gap-4"):
            for option in MODEL_CATALOG:
                with ui.card().classes("lopus-card p-5"):
                    ui.label(option.name).classes("text-xl font-bold")
                    ui.label(option.size).classes("text-blue-300")
                    ui.label(option.description).classes("lopus-muted text-sm")
                    ui.label(f"Ideal para: {option.recommended_for}").classes("lopus-muted text-xs")
                    ui.button("Selecionar", on_click=lambda option=option: select_model(option.id)).props("outline").classes("mt-3")
        status = ui.label("").classes("lopus-muted")
        progress = ui.spinner(size="lg")
        progress.set_visibility(False)
        async def download_and_continue() -> None:
            if not context.ollama.is_installed():
                ui.notify("Ollama não está instalado. Instale-o antes de baixar o modelo.", color="warning")
                return
            progress.set_visibility(True)
            status.set_text(f"Baixando {selected['model']}...")
            try:
                await context.ollama.pull(selected["model"], on_status=lambda line: status.set_text(line[-120:]))
            except (OllamaUnavailableError, RuntimeError) as exc:
                ui.notify(str(exc), color="negative")
                progress.set_visibility(False)
                return
            context.settings.provider = "ollama"
            context.settings.model = selected["model"]
            context.settings.setup_complete = True
            context.save()
            progress.set_visibility(False)
            ui.notify("Modelo configurado.", color="positive")
            ui.navigate.to("/home")
        def continue_demo() -> None:
            context.settings.provider = "demo"
            context.settings.setup_complete = True
            context.save()
            ui.navigate.to("/home")
        with ui.row().classes("gap-3"):
            ui.button("Baixar modelo e continuar", icon="download", on_click=download_and_continue)
            ui.button("Continuar em modo demo", icon="science", on_click=continue_demo).props("outline")
