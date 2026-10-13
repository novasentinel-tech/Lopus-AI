# Lopus-AI

O **Lopus-AI** é um projeto experimental de inteligência artificial autônoma com foco em construir, passo a passo, um **coworker digital local**.

A proposta inicial do projeto não é criar um novo modelo de linguagem do zero. O objetivo é desenvolver uma base modular capaz de utilizar modelos de IA, memória, ferramentas, plugins e subagentes para executar tarefas de forma progressivamente mais autônoma.

> **Estado atual:** estrutura inicial do projeto. Os módulos permanecem propositalmente simples para que sejam implementados, testados e documentados individualmente durante a evolução do Lopus.

## Objetivos

- Desenvolver o projeto publicamente como parte de um portfólio técnico.
- Manter uma arquitetura modular e compreensível.
- Permitir que o Lopus evolua para execução local na máquina do usuário.
- Implementar cada capacidade de forma incremental.
- Separar claramente capacidades internas, ferramentas e acessos externos.
- Permitir que o usuário controle quais recursos do computador e serviços externos a IA pode acessar.
- Explorar criação de subagentes para dividir tarefas complexas.
- Reduzir desperdício de contexto por meio de reorganização e compactação inteligente das conversas.

## Conceito

O Lopus deverá funcionar como uma camada de coordenação entre o usuário, modelos de IA e diferentes capacidades disponíveis no sistema.

Uma tarefa poderá envolver, por exemplo:

1. compreender o objetivo do usuário;
2. reorganizar o contexto atual;
3. decidir se a tarefa deve ser dividida;
4. criar subagentes quando necessário;
5. identificar quais ferramentas ou plugins são necessários;
6. solicitar permissões ao usuário;
7. executar as ações autorizadas;
8. reunir os resultados novamente no agente principal.

## Estrutura atual

```text
Lopus-AI/
├── docs/                       # Arquitetura e decisões técnicas
├── examples/                   # Exemplos pequenos de uso
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

A pasta `features/` reúne capacidades que pertencem ao próprio funcionamento do Lopus.

### Reorganização de contexto

`features/context_reorganization.py`

Essa feature deverá analisar o histórico da conversa e reorganizar as informações utilizadas pelo modelo. A ideia é preservar objetivos, decisões, restrições, tarefas pendentes e dados importantes enquanto reduz informações redundantes ou pouco relevantes.

Isso permitirá utilizar a janela de contexto de forma mais eficiente e diminuir o consumo desnecessário de tokens conforme uma sessão cresce.

### Subagentes

`features/subagents.py`

O Lopus poderá decidir que uma tarefa deve ser dividida em partes menores e criar subagentes especializados para trabalhar nelas.

Cada subagente deverá receber apenas o contexto, objetivo e permissões necessários para sua tarefa. O agente principal continuará responsável por acompanhar os resultados e consolidar o trabalho realizado.

## Plugins

A pasta `plugins/` representa capacidades que conectam o Lopus ao computador ou a serviços externos.

Plugins deverão operar dentro de um sistema explícito de permissões. O acesso a um recurso não deverá ser considerado automaticamente autorizado apenas porque o plugin está instalado.

### Permissões

`plugins/permissions.py`

Será responsável por controlar quais capacidades foram autorizadas pelo usuário, por quanto tempo e em qual escopo.

### Ponteiro virtual

`plugins/mouse_pointer.py`

A proposta é permitir que o Lopus tenha um **ponteiro virtual independente** para executar interações visuais autorizadas na interface do computador sem depender diretamente do ponteiro principal utilizado pelo usuário.

Esse módulo deverá possuir mecanismos claros de autorização, limitação e interrupção imediata.

### Google Drive

`plugins/google_drive.py`

Integração planejada para permitir que o Lopus trabalhe com arquivos do Google Drive após autorização do usuário.

A intenção é permitir fluxos como localizar documentos, criar arquivos, editar conteúdos, organizar pastas ou trabalhar durante uma tarefa mais longa sem exigir interação manual em cada etapa.

Credenciais, sessões e tokens de autenticação deverão ser tratados por uma camada segura e não deverão ser enviados desnecessariamente ao modelo de IA.

## Filosofia de desenvolvimento

O projeto começa propositalmente pequeno.

A ideia é construir cada módulo separadamente, entender sua função, implementar a lógica manualmente, testar e só então conectar a próxima parte do sistema.

O Lopus-AI será desenvolvido como um projeto em evolução contínua, documentando tanto decisões corretas quanto mudanças de arquitetura feitas durante o processo.

## Licença

Consulte o arquivo [LICENSE](LICENSE).
