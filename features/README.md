# Features

Cada capacidade de alto nível do Lopus deve possuir sua própria pasta.

Uma feature não deve controlar diretamente detalhes do sistema operacional quando já existir uma ação utilitária para isso. Por exemplo, a feature de documentos solicita `file.open`; quem decide como abrir o arquivo é a camada de ações, de acordo com as permissões e capacidades conectadas.

Estrutura atual:

```text
features/
├── context_reorganization/
├── documents/
└── subagents/
    └── models-subagents/
```

A intenção é manter cada feature isolada, documentada e evoluível sem transformar o runtime central em um bloco monolítico.
