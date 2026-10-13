# Interface local

A partir da versão 0.3.0, `lopus` inicia um painel local construído com NiceGUI.

## Fluxo

```text
lopus
  ↓
detectar ambiente
  ├── máquina local → NiceGUI em modo nativo
  └── GitHub Codespaces → NiceGUI web na porta 8080
  ↓
Setup inicial
  ├── detectar Ollama
  ├── escolher modelo
  └── baixar/configurar
  ↓
Painel
  ├── Home
  ├── Chat
  ├── Modelos
  ├── Features
  └── Plugins e permissões
```

Na máquina local, a interface e o backend são executados localmente e o NiceGUI utiliza uma janela desktop via pywebview.

No GitHub Codespaces, o Lopus detecta o ambiente automaticamente e desativa o modo nativo. O servidor escuta em `0.0.0.0:8080` para que a porta possa ser encaminhada pelo Codespaces.

## Comandos

Interface gráfica:

```bash
lopus
```

CLI antiga:

```bash
lopus-cli
```

## Testar o painel no GitHub Codespaces

O Codespaces é suportado apenas como ambiente de desenvolvimento e teste da interface. Recursos dependentes da máquina real, como ponteiro, aplicativos desktop e automação do sistema operacional, devem ser testados localmente.

No terminal do Codespace:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
lopus
```

O terminal exibirá que o painel está rodando em modo Codespaces na porta `8080`.

Depois:

1. abra a aba **Ports** do Codespaces;
2. localize a porta `8080`;
3. clique em **Open in Browser**.

Na primeira execução, use **Continuar em modo demo** se o objetivo for apenas validar o painel. Não é necessário instalar Ollama para testar navegação, features, plugins e configurações visuais.

A porta pode ser alterada com:

```bash
export LOPUS_UI_PORT=9000
lopus
```

## Detecção de ambiente

A classe `UIEnvironment` considera o ambiente como Codespaces quando encontra `CODESPACES=true` ou `GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN`.

Isso mantém o launcher com dois comportamentos:

```text
PC do usuário
→ native=True
→ janela desktop

GitHub Codespaces
→ native=False
→ servidor web encaminhado pelo GitHub
```

## Configuração persistente

O estado do painel é salvo em:

```text
~/.lopus/settings.json
```

O arquivo registra configurações como modelo ativo, features, plugins e permissões persistidas.

## Manifests

Cada feature deve possuir `features/<id>/manifest.json`.
Cada plugin apresentado na interface deve possuir `plugins/<id>/manifest.json`.

Assim novas capacidades podem aparecer automaticamente no painel sem criar cards específicos em código.
