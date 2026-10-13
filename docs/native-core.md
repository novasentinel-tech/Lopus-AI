# Native Core (C++)

A partir da versão 0.4.0, o Lopus possui uma camada nativa em C++ para operações de baixo nível.

## Princípio

C++ é uma implementação especializada, não a arquitetura principal.

```text
Feature / Agent
      ↓
Action
      ↓
NativeBridge (Python)
      ↓
lopus_native (pybind11)
      ↓
API do sistema operacional
```

Isso mantém features e agentes independentes da linguagem usada por baixo.

## Compilação

```bash
pip install -e .
```

O setuptools tenta compilar `lopus_native` usando pybind11 e C++20. A extensão foi marcada como opcional no processo de instalação: se o compilador nativo não estiver disponível, o restante do Lopus continua instalável e o painel informa que o Native Core está indisponível.

### Windows

Para utilizar o Native Core é necessário um compilador MSVC. O caminho recomendado é instalar **Visual Studio Build Tools** com **Desktop development with C++**. O módulo é linkado explicitamente com `User32` para as primitivas de cursor e tela.

### Codespaces / Linux

A extensão compila normalmente com GCC/Clang, mas as operações atuais de mouse retornam como não suportadas. Isso é proposital: o Codespaces é usado principalmente para testar painel e arquitetura.

## API nativa atual

```python
from lopus.native import NativeBridge

native = NativeBridge()
print(native.capabilities())
```

Quando disponível no Windows:

```python
x, y = native.cursor_position()
native.move_cursor(500, 300)
print(native.primary_screen_size())
```

## Actions

O runtime registra automaticamente:

- `system.native_info` — não requer permissão;
- `gui.cursor_position` — requer `gui.control`;
- `gui.move_cursor` — requer `gui.control`.

O backend nativo não ignora o sistema de permissões do Lopus. Features devem usar Actions, e não chamar `lopus_native` diretamente.

## Escopo atual

O movimento implementado nesta versão controla o cursor real do Windows. Ele **ainda não é o segundo ponteiro virtual** planejado para o Lopus.

O segundo ponteiro será uma camada própria, provavelmente combinando estado virtual, overlay e um executor nativo autorizado.

## Validação automática

O workflow `.github/workflows/native-ci.yml` compila o projeto em Ubuntu e Windows, em Python 3.11 e 3.12, importa `lopus_native` e executa a suíte de testes. Isso ajuda a evitar regressões entre a camada Python e o backend C++.
