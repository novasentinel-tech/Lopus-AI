# Primeiro MVP funcional

Esta versão estabelece o menor fluxo executável do Lopus-AI sem implementar ainda plugins, subagentes ou reorganização inteligente de contexto.

## Fluxo atual

```text
Usuário
  ↓
CLI
  ↓
LopusRuntime
  ├── SessionMemory
  └── ModelProvider
        ├── DemoProvider
        └── OllamaProvider
```

## Executar

Requer Python 3.11 ou superior.

```bash
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
pip install -e .
lopus
```

O provider padrão é `demo`, que testa o runtime sem utilizar uma LLM.

## Usar Ollama

Com Ollama instalado e um modelo já disponível:

PowerShell:

```powershell
$env:LOPUS_PROVIDER="ollama"
$env:LOPUS_MODEL="seu-modelo"
lopus
```

Ou diretamente:

```bash
lopus --provider ollama --model seu-modelo
```

O Lopus usa a API local do Ollama em `http://127.0.0.1:11434` por padrão.

## Testes

Após `pip install -e .`:

```bash
python -m unittest discover -s tests -v
```

## Fora do escopo deste MVP

- execução de plugins;
- controle de mouse;
- Google Drive;
- subagentes;
- memória persistente;
- reorganização inteligente de contexto;
- execução autônoma de tarefas.

Essas partes serão adicionadas e refinadas separadamente.
