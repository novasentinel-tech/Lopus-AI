# Plugins

Esta pasta reúne integrações que permitem ao Lopus-AI agir fora do próprio núcleo da aplicação.

Um plugin pode representar acesso ao sistema operacional, navegador, serviços online, arquivos ou outras ferramentas externas. Essas integrações devem respeitar permissões explícitas do usuário.

## Princípios

- Nenhum plugin deve assumir acesso automaticamente.
- O usuário deve saber qual capacidade está sendo solicitada.
- Permissões devem poder ser concedidas e revogadas.
- O agente principal e os subagentes devem respeitar o mesmo escopo de autorização.
- Credenciais e tokens não devem ser expostos ao modelo sem necessidade.

## Estrutura inicial

- `permissions.py` — gerenciamento do escopo de permissões.
- `mouse_pointer.py` — controle futuro de um ponteiro virtual independente para ações visuais.
- `google_drive.py` — integração futura com Google Drive, autenticação e operações autorizadas.

As implementações serão adicionadas módulo por módulo.
