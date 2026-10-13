# Lopus-AI

O **Lopus-AI** é um projeto pessoal e experimental de inteligência artificial autônoma, criado para estudar e desenvolver um agente local, modular e progressivamente capaz de utilizar modelos de IA, memória, ações, features, plugins, subagentes e uma camada nativa de baixo nível.

O projeto existe como espaço de pesquisa, aprendizado e desenvolvimento técnico. **Não possui objetivo financeiro ou comercial e não representa uma oferta de produto ou serviço.**

> **Estado atual:** painel local em NiceGUI + runtime agente com tool calling + Ollama + Actions/Permissions + Native Core em C++ + percepção de tela/OCR opcional.

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

`pip install -e .` tenta compilar a extensão C++ opcional `lopus_native`. No Windows, para o Native Core, é necessário ter Visual Studio Build Tools com suporte a C++.

Para instalar também a percepção visual/OCR local:

```powershell
pip install -e ".[vision]"
```

A CLI continua disponível:

```bash
lopus-cli
```

## O agente e as Actions

O Lopus não executa código Python arbitrário produzido pelo modelo. O modelo recebe um catálogo estruturado de Actions e pode solicitar chamadas de ferramentas. O runtime resolve a Action, verifica feature/plugin/permissões, executa e devolve o resultado ao modelo para que ele reavalie a tarefa.

```text
Usuário
  ↓
AgentExecutor
  ↓ conversa + schemas de Actions
Modelo local
  ↓ tool call estruturada
ActionRegistry
  ↓
PermissionStore
  ↓
Action Python
  ↓
NativeBridge / OCR / filesystem
  ↓ observação estruturada
Modelo local
  ↓
próxima Action ou resposta final
```

Existem limites de ciclos/chamadas e bloqueio de repetição para reduzir loops acidentais. `system.run_command` existe para uso controlado, mas **não é exposta ao agente autônomo por padrão**.

## Percepção e controle de tela

A feature **Percepção de Tela** usa o Native Core para capturar a tela principal no Windows e executa OCR local em Python.

Actions atuais incluem:

- `vision.read_screen` — lê textos e coordenadas visíveis;
- `vision.find_text` — procura um rótulo e retorna candidatos;
- `vision.click_text` — OCR → encontra texto → move → clica;
- `gui.cursor_position` — lê o cursor;
- `gui.move_cursor` — move o cursor;
- `gui.click` — clica em coordenadas;
- `gui.type_text` — digita texto Unicode.

Exemplo conceitual:

```text
"Clique em Configurações"
        ↓
vision.click_text("Configurações")
        ↓
captura BMP em C++
        ↓
OCR local
        ↓
centro do texto
        ↓
SetCursorPos + SendInput
        ↓
resultado volta ao modelo
```

Feature, plugin e permissão são travas independentes. Ter a implementação no código não significa que o modelo pode utilizá-la.

## Codespaces

No GitHub Codespaces o Lopus detecta o ambiente automaticamente e inicia o NiceGUI em modo web na porta `8080`.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
lopus
```

Use **PORTS → 8080 → Open in Browser**. Codespaces é indicado para testar painel, arquitetura, tool calling e lógica. As primitivas gráficas C++ atuais são Windows-only.

## Arquitetura

```text
Usuário
  ↓
NiceGUI
  ↓
Lopus Runtime
  ├── Model Provider
  ├── AgentExecutor
  ├── Memory
  ├── Action Registry
  └── Permission Store
        ↓
Features / Plugins
        ↓
Actions
  ├── Python
  ├── OCR
  └── NativeBridge
        ↓
  lopus_native (C++)
        ↓
Sistema operacional
```

### Features

Cada feature possui sua própria pasta e um `manifest.json`. O painel descobre esses manifests automaticamente. Features habilitadas controlam quais conjuntos de Actions entram no runtime.

### Plugins e permissões

Plugins representam recursos externos ou do sistema operacional. Ativar um plugin não concede automaticamente suas permissões. No runtime do painel, plugins habilitados também controlam quais Actions nativas são registradas.

Para o fluxo visual completo, atualmente são relevantes:

- feature `screen_perception`;
- plugin `screen_capture` + permissão `screen.capture`;
- plugin `mouse_pointer` + permissão `gui.control`;
- plugin `keyboard_input` + permissão `keyboard.control` para digitação.

### Native Core

O backend C++ é compilado como módulo Python via pybind11. No Windows ele implementa cursor, clique, teclado Unicode, tamanho da tela e captura BMP da tela principal usando Win32.

O movimento atual atua sobre o cursor real do Windows. O futuro **segundo ponteiro virtual** será uma camada separada.

## Painel local

O painel possui atualmente:

- **Início** — modelo, features, plugins, permissões e status do Native Core;
- **Chat** — conversa com o runtime e rastreamento das Actions executadas;
- **Modelos** — modelos instalados e catálogo sugerido;
- **Features** — descoberta automática via manifests;
- **Plugins** — integrações e permissões.

As configurações são persistidas em `~/.lopus/settings.json`.

## Documentação

- [`docs/agent-runtime.md`](docs/agent-runtime.md)
- [`docs/native-core.md`](docs/native-core.md)
- [`docs/actions.md`](docs/actions.md)
- [`docs/ui.md`](docs/ui.md)
- [`docs/mvp.md`](docs/mvp.md)
- [`docs/architecture.md`](docs/architecture.md)

## Licença e uso do código

Este projeto utiliza uma **licença proprietária de uso restrito**. O fato de o repositório estar publicamente visível não concede autorização para reutilizar o código.

Consulte [LICENSE](LICENSE).
