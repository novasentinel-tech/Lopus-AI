# Camada de ações

A camada `src/lopus/actions/` representa operações reutilizáveis que features e agentes podem solicitar sem conhecer os detalhes de execução.

Exemplo:

```text
DocumentFeature.open("relatorio.docx")
        ↓
ActionRegistry
        ↓
file.open
        ↓
PermissionStore
        ↓
OpenPathAction
        ├── native
        ├── shell
        └── GUI (quando um controlador/plugin estiver conectado)
```

## Princípios

1. uma feature descreve **o que precisa fazer**, não como clicar ou qual comando usar;
2. ações validam permissões antes de executar;
3. plugins fornecem capacidades externas, como controle gráfico ou serviços conectados;
4. o usuário continua responsável por conceder ou revogar permissões;
5. subagentes não recebem acesso automático só porque conhecem uma ação.

## Ações iniciais

- `file.inspect`
- `file.read_text`
- `file.write_text`
- `file.open`
- `system.run_command`

`system.run_command` exige `shell.execute`. `file.open` exige `file.open` e solicita permissões adicionais se o método escolhido for shell ou GUI.

## Próximas etapas

- escopos de permissão por pasta/arquivo;
- expiração de permissões;
- auditoria de ações;
- confirmação antes de ações destrutivas;
- adaptadores de GUI;
- integração da chamada de ações pelo modelo.
