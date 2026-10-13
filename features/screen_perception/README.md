# Percepção de Tela

Feature responsável por transformar a tela atual em observações estruturadas para o agente.

Fluxo atual:

```text
Native Core (C++)
  ↓ captura BMP da tela principal
RapidOCR (local)
  ↓
regiões de texto + confiança + coordenadas
  ↓
Actions vision.read_screen / vision.find_text
  ↓
AgentExecutor
```

## Instalação do OCR

A interface e o Native Core não exigem OCR para iniciar. Para habilitar leitura visual:

```bash
pip install -e ".[vision]"
```

## Permissões

- `screen.capture` para observar a tela;
- ações posteriores de mouse exigem `gui.control`;
- digitação exige `keyboard.control`.

Ativar esta feature não concede permissões automaticamente.
