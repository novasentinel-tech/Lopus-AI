# Documentos

Feature responsável por entender e trabalhar com documentos sem acoplar a lógica ao sistema operacional.

Princípio principal:

```text
Feature de documentos
        ↓
solicita uma ação
        ↓
ActionRegistry
        ↓
valida permissões
        ↓
método disponível
(native / shell / GUI / plugin futuro)
```

A primeira etapa implementa reconhecimento básico de estrutura e a capacidade de solicitar a abertura de um documento. Edição de DOCX/PDF, preservação avançada de layout e geração de conteúdo serão implementadas depois.
