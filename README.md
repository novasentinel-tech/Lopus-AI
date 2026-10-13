# Lopus-AI

O **Lopus-AI** é um projeto pessoal e experimental de inteligência artificial autônoma, criado para estudar e desenvolver um agente local, modular e progressivamente capaz de utilizar modelos de IA, memória, ações, features, plugins, subagentes e uma camada nativa de baixo nível.

O projeto existe como espaço de pesquisa, aprendizado e desenvolvimento técnico. **Não possui objetivo financeiro ou comercial e não representa uma oferta de produto ou serviço.**

> **Estado atual:** painel local em NiceGUI + runtime funcional + Ollama + Actions/Permissions + primeiro Native Core em C++.

## Executar

Requer Python 3.11 ou superior.

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\activate
pip install -e .
lopus
```

`pip install -e .` também compila a extensão C++ `lopus_native`. No Windows é necessário ter o Visual Studio Build Tools com suporte a C++ instalado.

A CLI continua disponível:

```bash
lopus-cli
```

## Codespaces

No GitHub Codespaces o Lopus detecta o ambiente automaticamente e inicia o NiceGUI em modo web na porta `8080`.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
lopus
```

Use **PORTS → 8080 → Open in Browser**. O Codespaces é indicado para testar painel, arquitetura e lógica; integrações reais com mouse e desktop devem ser testadas na máquina local.

## Arquitetura

```text
Usuário
  ↓
NiceGUI
  ↓
Lopus Runtime
  ├── Model Provider
  ├── Memory
  ├── Action Registry
  └── Permission Store
        ↓
Features / Agents
        ↓
Actions
  ├── Python
  └── NativeBridge
        ↓
  lopus_native (C++)
        ↓
Plugins / sistema operacional
```

### Features

Cada feature possui sua própria pasta e um `manifest.json`. O painel descobre esses manifests automaticamente.

### Actions

Ações são operações utilitárias reutilizáveis. Features solicitam Actions em vez de acoplar diretamente lógica de shell, filesystem, GUI ou C++.

### Native Core

O primeiro backend C++ é compilado como módulo Python via pybind11. Atualmente ele fornece informações nativas do processo e, no Windows, primitivas de cursor/tela.

O runtime expõe essas primitivas por Actions protegidas:

- `system.native_info`;
- `gui.cursor_position` (`gui.control`);
- `gui.move_cursor` (`gui.control`).

O movimento atual atua sobre o cursor real do Windows. O futuro **segundo ponteiro virtual** será implementado como uma camada separada.

### Plugins e permissões

Plugins representam acesso a recursos externos ou ao sistema operacional. Ativar um plugin **não concede automaticamente suas permissões**.

## Painel local

O painel possui atualmente:

- **Início** — modelo, features, plugins, permissões e status do Native Core;
- **Chat** — conversa com o runtime configurado;
- **Modelos** — modelos instalados e catálogo sugerido;
- **Features** — descoberta automática via manifests;
- **Plugins** — integrações e permissões.

As configurações são persistidas em `~/.lopus/settings.json`.

## Documentação

- [`docs/mvp.md`](docs/mvp.md)
- [`docs/actions.md`](docs/actions.md)
- [`docs/ui.md`](docs/ui.md)
- [`docs/native-core.md`](docs/native-core.md)
- [`docs/architecture.md`](docs/architecture.md)

## Licença e uso do código

Este projeto utiliza uma **licença proprietária de uso restrito**. O fato de o repositório estar publicamente visível não concede autorização para reutilizar o código.

Consulte [LICENSE](LICENSE).
