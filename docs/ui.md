# Interface local

A partir da versão 0.3.0, `lopus` inicia um painel local construído com NiceGUI.

## Fluxo

```text
lopus
  ↓
NiceGUI em modo nativo
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

A interface e o backend são executados na máquina local. O modo nativo utiliza a janela desktop do NiceGUI/pywebview.

## Comandos

Interface gráfica:

```bash
lopus
```

CLI antiga:

```bash
lopus-cli
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
