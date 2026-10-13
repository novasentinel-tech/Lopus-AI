# Subagentes

Esta feature será responsável por criar, configurar, acompanhar e encerrar agentes temporários especializados.

Os perfis iniciais ficam em `models-subagents/`. Neste estágio eles são **perfis de comportamento**, não pesos de modelos de IA.

Perfis iniciais:

- `mathematics.json` — matemática e raciocínio quantitativo;
- `documents.json` — estrutura e produção de documentos;
- `programming.json` — código, depuração e arquitetura;
- `screen_organization.json` — organização de janelas e interface, sempre sujeita a permissões.

O agente principal deverá decidir futuramente quando delegar uma tarefa e qual contexto mínimo cada subagente receberá.
