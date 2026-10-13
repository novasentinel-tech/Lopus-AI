# Lopus-AI

O **Lopus-AI** é um projeto pessoal e experimental de inteligência artificial autônoma, criado para estudar e desenvolver, passo a passo, uma base capaz de executar tarefas localmente, utilizar ferramentas autorizadas pelo usuário, reorganizar contexto e coordenar subagentes.

O projeto existe principalmente como espaço de pesquisa, aprendizado e desenvolvimento técnico. **Não possui objetivo financeiro ou comercial e não representa uma oferta de produto ou serviço.**

A intenção é construir cada parte de forma progressiva, mantendo a arquitetura compreensível e permitindo que o funcionamento interno do sistema seja estudado durante sua evolução.

> **Estado atual:** estrutura inicial. Os módulos ainda serão implementados e testados individualmente.

## Ideia central

O Lopus-AI pretende evoluir para um agente local capaz de trabalhar de maneira mais autônoma dentro dos limites e permissões definidos pelo usuário.

Em vez de concentrar toda a lógica em um único componente, o projeto será dividido em módulos independentes responsáveis por tarefas como:

- gerenciamento do runtime principal;
- comunicação com modelos de IA;
- memória e preservação de contexto;
- reorganização de conversas extensas;
- criação e coordenação de subagentes;
- uso de ferramentas internas;
- plugins para interação com o computador e serviços externos;
- controle explícito de permissões.

## Funcionamento planejado

Uma tarefa poderá seguir um fluxo semelhante a:

1. receber um objetivo do usuário;
2. interpretar o contexto disponível;
3. reorganizar ou resumir informações quando necessário;
4. decidir se a tarefa deve ser dividida;
5. criar subagentes especializados quando fizer sentido;
6. identificar ferramentas ou plugins necessários;
7. solicitar ao usuário as permissões exigidas;
8. executar apenas as ações autorizadas;
9. acompanhar o progresso;
10. reunir os resultados no agente principal.

Nada relacionado ao acesso ao computador ou a serviços externos deverá ser considerado automaticamente autorizado.

## Estrutura atual

```text
Lopus-AI/
├── docs/                       # Arquitetura e decisões técnicas
├── examples/                   # Exemplos de uso
│
├── features/                   # Capacidades internas do Lopus
│   ├── README.md
│   ├── context_reorganization.py
│   └── subagents.py
│
├── plugins/                    # Integrações externas e acesso autorizado
│   ├── README.md
│   ├── permissions.py
│   ├── mouse_pointer.py
│   └── google_drive.py
│
├── src/
│   └── lopus/
│       ├── agents/             # Agentes e comportamentos autônomos
│       ├── core/               # Runtime principal e orquestração
│       ├── interfaces/         # CLI, API e futuras interfaces
│       ├── memory/             # Memória de curto e longo prazo
│       ├── models/             # Adaptadores e roteamento de modelos
│       └── tools/              # Ferramentas executáveis pelo runtime
│
├── tests/                      # Testes automatizados
├── .env.example
├── .gitignore
├── LICENSE
└── pyproject.toml
```

## Features

A pasta `features/` reúne capacidades pertencentes ao funcionamento interno do Lopus.

### Reorganização de contexto

`features/context_reorganization.py`

Essa feature será responsável por analisar conversas ou sessões extensas e reorganizar as informações relevantes para o modelo.

A intenção é preservar elementos como objetivos, decisões, restrições, tarefas pendentes e informações importantes enquanto reduz redundância e conteúdo pouco útil para a execução atual.

Esse mecanismo também poderá ajudar a diminuir o desperdício de tokens e permitir sessões mais longas sem carregar continuamente todo o histórico bruto.

### Subagentes

`features/subagents.py`

O agente principal poderá dividir determinadas tarefas em partes menores e criar subagentes temporários para executá-las.

Cada subagente deverá receber apenas o contexto, objetivo, ferramentas e permissões necessários para sua função. O agente principal continuará responsável por acompanhar e consolidar os resultados.

## Plugins

A pasta `plugins/` reúne módulos que conectam o Lopus ao sistema operacional ou a serviços externos.

Plugins deverão depender de permissões explícitas do usuário e operar somente dentro do escopo autorizado.

### Permissões

`plugins/permissions.py`

Responsável por controlar quais capacidades externas estão disponíveis para o Lopus, além do escopo e duração de cada autorização.

### Ponteiro virtual

`plugins/mouse_pointer.py`

Experimento planejado para permitir que o Lopus opere um **ponteiro virtual independente**, destinado a interações visuais autorizadas com a interface do computador.

A implementação deverá possuir mecanismos claros de autorização, limitação, observação e interrupção imediata pelo usuário.

### Google Drive

`plugins/google_drive.py`

Integração planejada para permitir que o Lopus trabalhe com arquivos do Google Drive quando autorizado.

A ideia é estudar fluxos em que o agente possa localizar, organizar, criar ou editar conteúdos durante uma tarefa, sem expor credenciais e tokens desnecessariamente ao modelo de linguagem.

## Desenvolvimento

O Lopus-AI será desenvolvido de forma incremental.

A prioridade é compreender e implementar cada módulo individualmente antes de adicionar novas camadas de complexidade. Mudanças de arquitetura, experimentos que não funcionarem e decisões técnicas relevantes poderão ser documentados junto com a evolução do projeto.

O fato de o código estar disponível publicamente neste repositório tem finalidade de acompanhamento e demonstração do desenvolvimento e **não concede autorização para reutilização**.

## Licença e uso do código

Este projeto utiliza uma **licença proprietária de uso restrito**.

O código pode ser visualizado neste repositório, porém não é software livre nem open source. Nenhuma permissão é concedida para copiar, reutilizar, executar, modificar, redistribuir, sublicenciar, incorporar ou criar trabalhos derivados a partir do código, total ou parcialmente, sem autorização prévia e expressa do titular dos direitos.

Consulte os termos completos em [LICENSE](LICENSE).
