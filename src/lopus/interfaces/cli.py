"""Interface de terminal do primeiro MVP do Lopus-AI."""

from __future__ import annotations

import argparse
import json

from lopus import __version__
from lopus.config import LopusConfig
from lopus.core.runtime import LopusRuntime
from lopus.memory.session import SessionMemory
from lopus.models.base import ModelError
from lopus.models.factory import create_model


def build_runtime(config: LopusConfig) -> LopusRuntime:
    return LopusRuntime(
        model=create_model(config),
        memory=SessionMemory(max_messages=config.max_messages),
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Lopus-AI — runtime experimental local")
    parser.add_argument("--provider", choices=("demo", "ollama"), help="Provider de modelo")
    parser.add_argument("--model", help="Nome do modelo local (quando usar Ollama)")
    parser.add_argument("--prompt", help="Executa uma única mensagem e encerra")
    parser.add_argument("--version", action="version", version=f"Lopus-AI {__version__}")
    return parser


def _show_help() -> None:
    print("Comandos:")
    print("  /help    mostra esta ajuda")
    print("  /status  mostra o estado atual do runtime")
    print("  /clear   limpa a memória da sessão")
    print("  /exit    encerra o Lopus")


def _run_once(runtime: LopusRuntime, prompt: str) -> int:
    try:
        print(runtime.reply(prompt))
        return 0
    except (ModelError, ValueError) as exc:
        print(f"Erro: {exc}")
        return 1


def main() -> None:
    args = _parser().parse_args()
    config = LopusConfig.from_env().with_overrides(provider=args.provider, model=args.model)
    runtime = build_runtime(config)

    if args.prompt:
        raise SystemExit(_run_once(runtime, args.prompt))

    print(f"Lopus-AI {__version__}")
    print(f"Provider: {config.provider}" + (f" | Modelo: {config.model}" if config.provider == "ollama" else ""))
    print("Digite /help para ver os comandos.\n")

    while True:
        try:
            user_input = input("Você > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando Lopus.")
            break

        if not user_input:
            continue
        if user_input == "/exit":
            print("Encerrando Lopus.")
            break
        if user_input == "/help":
            _show_help()
            continue
        if user_input == "/clear":
            runtime.clear()
            print("Memória da sessão limpa.")
            continue
        if user_input == "/status":
            print(json.dumps(runtime.status(), ensure_ascii=False, indent=2))
            continue

        try:
            print(f"Lopus > {runtime.reply(user_input)}\n")
        except (ModelError, ValueError) as exc:
            print(f"Erro > {exc}\n")
