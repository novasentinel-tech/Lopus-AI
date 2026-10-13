# Lopus Native Core

Esta pasta contém o backend C++ do Lopus-AI.

O objetivo não é mover a arquitetura do projeto para C++. O Native Core existe para operações de baixo nível, integração com o sistema operacional e rotinas em que Python não seja a camada ideal.

## Build

A extensão é compilada como `lopus_native` durante:

```bash
pip install -e .
```

O build usa **pybind11 + setuptools** e requer um compilador C++20.

### Windows

Instale o Visual Studio Build Tools com o workload **Desktop development with C++**.

### Linux / Codespaces

Um compilador GCC/Clang compatível com C++20 é suficiente.

## Capacidades atuais

- identificar a plataforma nativa;
- obter o PID do processo;
- informar se o backend de entrada gráfica é suportado;
- Windows: obter posição do cursor;
- Windows: mover o cursor;
- Windows: obter resolução da tela principal.

As operações de cursor são intencionalmente protegidas no runtime por `gui.control`.

## Próximas áreas

```text
native/
├── system        # processos, janelas e informações do SO
├── input         # mouse/teclado e futuro ponteiro virtual
├── capture       # captura de tela
└── ipc           # comunicação com serviços nativos futuros
```
