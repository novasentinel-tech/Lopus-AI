"""Interface de terminal do Lopus-AI."""

from __future__ import annotations

import argparse
import json

from lopus import __version__
from lopus.actions import ActionError, Permission, PermissionDeniedError
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
    print("  /help                       mostra esta ajuda")
    print("  /status                     mostra o estado do runtime")
    print("  /actions                    lista ações utilitárias disponíveis")
    print("  /permissions                lista permissões concedidas")
    print("  /grant <permissão>          concede uma permissão nesta sessão")
    print("  /revoke <permissão>         revoga uma permissão nesta sessão")
    print("  /open <caminho>             abre arquivo/pasta pelo sistema")
    print("  /clear                      limpa a memória da sessão")
    print("  /exit                       encerra o Lopus")
    print("\nPermissões conhecidas:")
    for permission in Permission:
        print(f"  {permission.value}")


def _run_once(runtime: LopusRuntime, prompt: str) -> int:
    try:
        print(runtime.reply(prompt))
        return 0
    except (ModelError, ValueError) as exc:
        print(f"Erro: {exc}")
        return 1


def _handle_runtime_command(runtime: LopusRuntime, user_input: str) -> bool:
    if user_input == "/help":
        _show_help()
        return True

    if user_input == "/status":
        print(json.dumps(runtime.status(), ensure_ascii=False, indent=2))
        return True

    if user_input == "/actions":
        for name in runtime.actions.names():
            action = runtime.actions.get(name)
            permissions = ", ".join(
                permission.value for permission in action.required_permissions
            ) or "nenhuma"
            print(f"- {name}: {action.description} [permissões: {permissions}]")
        return True

    if user_input == "/permissions":
        grants = runtime.permissions.snapshot()
        if not grants:
            print("Nenhuma permissão concedida nesta sessão.")
        else:
            for grant in grants:
                print(f"- {grant.permission.value} (por {grant.granted_by})")
        return True

    if user_input.startswith("/grant "):
        raw = user_input.removeprefix("/grant ").strip()
        try:
            runtime.grant_permission(raw)
            print(f"Permissão concedida nesta sessão: {raw}")
        except ValueError:
            print(f"Permissão desconhecida: {raw}")
        return True

    if user_input.startswith("/revoke "):
        raw = user_input.removeprefix("/revoke ").strip()
        try:
            runtime.revoke_permission(raw)
            print(f"Permissão revogada: {raw}")
        except ValueError:
            print(f"Permissão desconhecida: {raw}")
        return True

    if user_input.startswith("/open "):
        path = user_input.removeprefix("/open ").strip().strip('"')
        try:
            result = runtime.execute_action("file.open", path=path)
            print(result.message)
        except (ActionError, PermissionDeniedError, OSError) as exc:
            print(f"Ação bloqueada: {exc}")
        return True

    if user_input == "/clear":
        runtime.clear()
        print("Memória da sessão limpa.")
        return True

    return False


def main() -> None:
    args = _parser().parse_args()
    config = LopusConfig.from_env().with_overrides(provider=args.provider, model=args.model)
    runtime = build_runtime(config)

    if args.prompt:
        raise SystemExit(_run_once(runtime, args.prompt))

    print(f"Lopus-AI {__version__}")
    print(
        f"Provider: {config.provider}"
        + (f" | Modelo: {config.model}" if config.provider == "ollama" else "")
    )
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
        if _handle_runtime_command(runtime, user_input):
            continue

        try:
            print(f"Lopus > {runtime.reply(user_input)}\n")
        except (ModelError, ValueError) as exc:
            print(f"Erro > {exc}\n")
