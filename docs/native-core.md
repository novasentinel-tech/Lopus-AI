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

O setuptools compila `lopus_native` usando pybind11 e C++20.

### Windows

É necessário um compilador MSVC. O caminho recomendado é instalar **Visual Studio Build Tools** com **Desktop development with C++**.

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
