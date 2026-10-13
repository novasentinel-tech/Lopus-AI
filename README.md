# Lopus-AI

O **Lopus-AI** é um projeto pessoal e experimental de inteligência artificial autônoma, criado para estudar e desenvolver um agente local, modular e progressivamente capaz de utilizar modelos de IA, memória, ações, features, plugins e subagentes.

O projeto existe como espaço de pesquisa, aprendizado e desenvolvimento técnico. **Não possui objetivo financeiro ou comercial e não representa uma oferta de produto ou serviço.**

> **Estado atual:** painel desktop local em NiceGUI + runtime funcional + integração com modelos locais por Ollama.

## Executar

Requer Python 3.11 ou superior.

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\activate
pip install -e .
lopus
```

`lopus` abre o painel local em modo nativo.

A CLI anterior continua disponível:

```bash
lopus-cli
```

## Testar no GitHub Codespaces

O Codespaces pode ser usado para testar o painel e a navegação sem depender do ambiente desktop real.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
lopus
```

O Lopus detecta o Codespaces automaticamente e inicia o NiceGUI em modo web na porta `8080`. Depois, abra a aba **Ports** do Codespaces e use **Open in Browser** na porta `8080`.

Para testar somente a interface, escolha **Continuar em modo demo** no setup inicial. Plugins que dependem do sistema operacional, mouse, aplicativos desktop ou recursos locais devem ser testados na máquina real.

## Painel local

Na primeira execução, o Lopus abre um assistente de configuração para:

1. detectar o Ollama;
2. escolher um modelo local;
3. baixar o modelo;
4. definir o modelo ativo;
5. entrar no painel principal.

O painel atual contém:

- **Início** — resumo do estado do sistema;
- **Chat** — conversa com o runtime configurado;
- **Modelos** — modelos instalados e catálogo sugerido;
- **Features** — capacidades internas descobertas por manifest;
- **Plugins** — integrações externas e permissões do runtime.

As configurações são persistidas localmente em `~/.lopus/settings.json`.

## Arquitetura

```text
Usuário
  ↓
NiceGUI
  ↓
Lopus Runtime
  ├── Model Provider
  ├── Memory
  ├── Action Registry
  └── Permission Store
        ↓
Features
  ├── context_reorganization/
  ├── documents/
  └── subagents/
        ↓
Actions
        ↓
Plugins / sistema operacional
```

### Features

Cada feature possui sua própria pasta e um `manifest.json`. O painel descobre esses manifests automaticamente.

### Actions

Ações são operações utilitárias reutilizáveis, como `file.inspect`, `file.read_text`, `file.write_text`, `file.open` e `system.run_command`. Uma feature solicita uma ação; a ação valida permissões e decide como executar.

### Plugins

Plugins representam acesso a recursos externos ou ao sistema operacional. Ativar um plugin **não concede automaticamente suas permissões**.

## Modelos locais

O painel usa o Ollama como primeiro runtime local. O catálogo inicial contém sugestões compactas, mas outros modelos instalados no Ollama também podem ser usados.

## Documentação

- [`docs/mvp.md`](docs/mvp.md)
- [`docs/actions.md`](docs/actions.md)
- [`docs/ui.md`](docs/ui.md)
- [`docs/architecture.md`](docs/architecture.md)

## Licença e uso do código

Este projeto utiliza uma **licença proprietária de uso restrito**. O fato de o repositório estar publicamente visível não concede autorização para reutilizar o código.

Consulte [LICENSE](LICENSE).
