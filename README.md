# Lopus-AI

O **Lopus-AI** é um projeto pessoal e experimental de inteligência artificial autônoma, criado para estudar uma arquitetura local, modular e progressivamente capaz de executar tarefas com modelos de IA, memória, ações, features, plugins e subagentes.

O projeto existe como espaço de pesquisa, aprendizado e desenvolvimento técnico. **Não possui objetivo financeiro ou comercial e não representa uma oferta de produto ou serviço.**

> **Versão atual:** `0.2.0` — runtime funcional de terminal + primeira camada de ações utilitárias e permissões.

## O que já funciona

- interface de terminal (`lopus`);
- runtime central;
- memória volátil da sessão;
- provider de demonstração e provider local via Ollama;
- registro de ações utilitárias;
- permissões de sessão;
- leitura, escrita e inspeção básica de arquivos de texto;
- abertura de arquivos/pastas pelo sistema;
- execução explícita de comandos com permissão;
- estrutura modular de features;
- perfis iniciais de subagentes;
- testes básicos de memória, runtime e ações.

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

Para usar um modelo local com Ollama:

```bash
lopus --provider ollama --model seu-modelo
```

## Permissões no terminal

As ações externas começam sem permissão.

Exemplo para permitir que o runtime abra um arquivo durante a sessão:

```text
/grant file.open
/open "C:\caminho\arquivo.docx"
```

Use `/permissions` para conferir permissões e `/revoke file.open` para revogar.

## Organização

```text
Lopus-AI/
├── docs/
│   ├── architecture.md
│   ├── actions.md
│   └── mvp.md
├── features/
│   ├── context_reorganization/
│   │   └── feature.py
│   ├── documents/
│   │   ├── feature.py
│   │   └── structure.py
│   └── subagents/
│       ├── manager.py
│       └── models-subagents/
│           ├── mathematics.json
│           ├── documents.json
│           ├── programming.json
│           └── screen_organization.json
├── plugins/
│   ├── permissions.py
│   ├── mouse_pointer.py
│   └── google_drive.py
├── src/lopus/
│   ├── actions/
│   ├── agents/
│   ├── core/
│   ├── interfaces/
│   ├── memory/
│   ├── models/
│   └── tools/
└── tests/
```

## Actions, Features e Plugins

**Action** é uma operação reutilizável e pequena, como `file.open` ou `file.read_text`.

**Feature** é uma capacidade maior, como trabalhar com documentos. Ela combina estrutura, regras e várias ações.

**Plugin** conecta o Lopus a algo externo, como GUI, Google Drive ou outro serviço. O plugin não deve ganhar acesso automaticamente: as permissões continuam sob controle do usuário.

Isso permite que uma feature de documentos peça apenas:

```text
"abra este documento"
```

sem precisar saber se o runtime vai usar integração nativa do sistema, PowerShell/Bash ou, futuramente, cliques por um controlador gráfico autorizado.

## Subagentes

A feature `subagents/` possui perfis especializados iniciais para matemática, documentos, programação e organização da tela.

Esses perfis não são modelos treinados e não recebem permissões automaticamente. Eles descrevem funções especializadas que poderão ser atribuídas a agentes temporários no futuro.

## Desenvolvimento

O Lopus será evoluído feature por feature. A intenção é melhorar cada módulo isoladamente antes de aumentar a autonomia do sistema.

A arquitetura de ações está documentada em [`docs/actions.md`](docs/actions.md).

## Licença e uso do código

Este projeto utiliza uma **licença proprietária de uso restrito**. O fato de o repositório estar publicamente visível não concede autorização para reutilizar o código.

Consulte os termos completos em [LICENSE](LICENSE).
