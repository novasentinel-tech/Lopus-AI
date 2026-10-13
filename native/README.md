# Lopus Native Core

Esta pasta contém o backend C++ de baixo nível do Lopus-AI.

O objetivo não é mover a arquitetura para C++. O Native Core fornece primitivas do sistema operacional; Python continua responsável por runtime, Actions, features, permissões, OCR e raciocínio do agente.

## Build

A extensão é compilada como `lopus_native` durante:

```bash
pip install -e .
```

O build usa **pybind11 + setuptools** e requer um compilador C++20. A extensão é opcional: se não puder ser compilada, o painel Python ainda pode iniciar e reportará o Native Core como indisponível.

### Windows

Instale o Visual Studio Build Tools com o workload **Desktop development with C++**.

O backend Windows usa atualmente `User32` e `Gdi32`.

### Linux / Codespaces

Um compilador GCC/Clang compatível com C++20 é suficiente para compilar o módulo e testar contratos básicos. As primitivas gráficas atuais permanecem Windows-only.

## Capacidades atuais

Gerais:

- identificar plataforma;
- obter PID do processo;
- informar suporte de entrada gráfica;
- informar suporte de captura de tela.

Windows:

- posição atual do cursor (`GetCursorPos`);
- movimento do cursor (`SetCursorPos`);
- clique esquerdo/direito/meio (`SendInput`);
- digitação Unicode (`SendInput` + `KEYEVENTF_UNICODE`);
- tamanho da tela principal (`GetSystemMetrics`);
- captura da tela principal em BMP (`BitBlt` + `GetDIBits`).

## Como o agente usa o C++

O modelo nunca chama C++ diretamente:

```text
Modelo
  ↓ tool call
AgentExecutor
  ↓
Action Python
  ↓ permissões
NativeBridge
  ↓
lopus_native (pybind11)
  ↓
Win32
```

Exemplo: `gui.click` valida `gui.control`, chama `NativeBridge.move_cursor`, depois `NativeBridge.click_mouse`, que finalmente executa as primitivas Win32.

Para percepção visual, C++ captura a tela e Python executa OCR local. Veja [`docs/agent-runtime.md`](../docs/agent-runtime.md).

## Importante: ponteiro atual

O backend atual controla o **cursor real do sistema operacional**. Ele ainda não implementa o conceito planejado de um segundo ponteiro virtual independente. Isso será uma camada futura, separada das primitivas atuais.

## Próximas áreas

```text
native/
├── system        # processos, janelas e informações do SO
├── input         # mouse/teclado e futuro ponteiro virtual
├── capture       # captura otimizada / por janela
└── ipc           # comunicação com serviços nativos futuros
```
