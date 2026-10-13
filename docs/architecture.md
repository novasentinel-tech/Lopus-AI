# Arquitetura do Lopus-AI

O Lopus é dividido em camadas para evitar que uma feature precise conhecer detalhes de sistema operacional, autenticação ou interface gráfica.

```text
Usuário
  ↓
Interface
  ↓
LopusRuntime
  ├── Modelo
  ├── Memória
  ├── PermissionStore
  └── ActionRegistry
         ↑
      Features
         ↑
      Subagentes
         ↓
      Plugins / SO / serviços externos
```

## Runtime

Coordena conversa, memória, providers, permissões e ações disponíveis.

## Actions

Operações reutilizáveis e controladas por permissão. Exemplos: abrir um arquivo, ler texto ou executar um comando autorizado.

## Features

Capacidades de alto nível. Cada feature possui uma pasta própria. A feature deve solicitar ações ao runtime em vez de implementar diretamente automação de sistema.

## Plugins

Adaptadores externos. Um plugin pode oferecer controle de GUI, integração com um serviço ou outra capacidade que não pertence ao núcleo.

## Subagentes

Perfis especializados que futuramente poderão receber objetivos menores. Eles não herdam acesso irrestrito; ações e permissões continuam sendo controladas pelo runtime.
