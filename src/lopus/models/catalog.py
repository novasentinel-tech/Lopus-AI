"""Catálogo inicial de modelos locais sugeridos pelo Lopus."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ModelOption:
    id: str
    name: str
    size: str
    description: str
    recommended_for: str


MODEL_CATALOG: tuple[ModelOption, ...] = (
    ModelOption(id="llama3.2:3b", name="Llama 3.2 3B", size="~2.0 GB", description="Modelo leve e multilíngue para uso geral.", recommended_for="máquinas com pouca memória e testes iniciais"),
    ModelOption(id="qwen3:4b", name="Qwen3 4B", size="~2.5 GB", description="Modelo compacto com foco forte em raciocínio e ferramentas.", recommended_for="uso geral, programação e agentes"),
    ModelOption(id="gemma3:4b", name="Gemma 3 4B", size="~3.4 GB", description="Modelo compacto multimodal da família Gemma.", recommended_for="uso geral e experimentos multimodais"),
)


def get_model_option(model_id: str) -> ModelOption | None:
    return next((item for item in MODEL_CATALOG if item.id == model_id), None)
