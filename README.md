# Lopus-AI

O **Lopus-AI** é um projeto pessoal e experimental de inteligência artificial autônoma, criado para estudar e desenvolver uma base local, modular e progressivamente capaz de executar tarefas com modelos de IA, memória, ferramentas, plugins e subagentes.

O projeto existe como espaço de pesquisa, aprendizado e desenvolvimento técnico. **Não possui objetivo financeiro ou comercial e não representa uma oferta de produto ou serviço.**

> **Estado atual:** primeiro MVP funcional de terminal. O runtime já pode operar em modo de demonstração ou conversar com um modelo local por meio do Ollama.

## O que já funciona

- interface de terminal (`lopus`);
- runtime central;
- memória volátil da sessão;
- contrato comum para providers de modelos;
- provider de demonstração sem LLM;
- provider local via Ollama;
- comandos de status, limpeza da sessão e saída;
- testes básicos do runtime e da memória.

## Executar o MVP

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

Por padrão, o Lopus inicia em `demo`, permitindo validar toda a arquitetura sem depender de um modelo.

### Modelo local com Ollama

Com Ollama instalado e um modelo disponível:

```bash
lopus --provider ollama --model seu-modelo
```

Também é possível configurar pelas variáveis descritas em `.env.example`.

## Estrutura

```text
Lopus-AI/
├── docs/                       # arquitetura e documentação técnica
├── examples/                   # exemplos futuros
├── features/                   # features experimentais desenvolvidas separadamente
│   ├── context_reorganization.py
│   └── subagents.py
├── plugins/                    # integrações e acessos sujeitos a permissão
│   ├── permissions.py
│   ├── mouse_pointer.py
│   └── google_drive.py
├── src/lopus/
│   ├── agents/                 # comportamento do agente principal
│   ├── core/                   # runtime e tipos centrais
│   ├── interfaces/             # CLI e interfaces futuras
│   ├── memory/                 # memória da sessão
│   ├── models/                 # providers de modelos
│   └── tools/                  # registro de ferramentas
├── tests/
├── .env.example
├── LICENSE
└── pyproject.toml
```

## Direção do projeto

O desenvolvimento será incremental. Features como reorganização de contexto, subagentes, plugins, ponteiro virtual, integrações externas e execução autônoma serão implementadas e melhoradas uma por uma.

Nenhum acesso ao computador, navegador, arquivos ou serviços externos deverá ser presumido. Capacidades externas deverão depender de autorização explícita e de escopo definido pelo usuário.

A documentação do primeiro MVP está em [`docs/mvp.md`](docs/mvp.md).

## Licença e uso do código

Este projeto utiliza uma **licença proprietária de uso restrito**. O fato de o repositório estar publicamente visível não concede autorização para reutilizar o código.

Consulte os termos completos em [LICENSE](LICENSE).
