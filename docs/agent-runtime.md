# Runtime de ações do agente

Esta versão define como uma decisão do modelo se transforma em uma ação real no computador sem executar código arbitrário produzido pela IA.

## Fluxo

```text
Usuário
  ↓
LopusRuntime
  ↓
AgentExecutor
  ↓ envia conversa + schemas de Actions
ModelProvider / Ollama
  ↓ tool_call estruturada
ActionRegistry
  ↓ resolve alias da tool
PermissionStore
  ↓ valida permissões
Action Python
  ↓
NativeBridge / OCR / filesystem / plugin
  ↓
resultado estruturado
  ↓ mensagem role=tool
ModelProvider
  ↓ reavalia o estado
próxima Action ou resposta final
```

## Exemplo

O usuário pede:

> Clique em Configurações.

O modelo não escreve nem executa uma linha Python. Ele pode solicitar uma função estruturada equivalente a:

```json
{
  "name": "vision__click_text",
  "arguments": {
    "query": "Configurações"
  }
}
```

`ActionRegistry` mapeia `vision__click_text` para a Action interna `vision.click_text`.

Essa Action exige:

- feature `screen_perception` habilitada;
- plugin `screen_capture` habilitado;
- plugin `mouse_pointer` habilitado;
- permissão `screen.capture`;
- permissão `gui.control`.

Quando tudo está disponível:

```text
vision.click_text
  ↓
NativeBridge.capture_primary_screen_bmp()
  ↓
C++ / Win32 captura a tela
  ↓
RapidOCR identifica textos e caixas
  ↓
Lopus escolhe o melhor candidato
  ↓
centro da caixa OCR
  ↓
NativeBridge.move_cursor(x, y)
  ↓
NativeBridge.click_mouse("left")
  ↓
C++ / Win32 executa SetCursorPos + SendInput
```

O resultado volta ao modelo como uma observação da ferramenta. O modelo pode então encerrar, observar a tela novamente ou escolher outra Action.

## Actions visuais atuais

- `vision.read_screen`: lê o estado textual geral da tela via OCR;
- `vision.find_text`: procura um rótulo e retorna candidatos/centros;
- `vision.click_text`: procura e clica no melhor candidato textual;
- `gui.cursor_position`: lê a posição do cursor;
- `gui.move_cursor`: move o cursor por coordenada;
- `gui.click`: move e clica por coordenada;
- `gui.type_text`: digita texto Unicode no foco atual.

## Limites do loop

Para reduzir loops acidentais:

- máximo de 8 ciclos de decisão por tarefa;
- máximo de 20 chamadas de Actions;
- repetição idêntica de Action + argumentos é limitada;
- erros e permissões negadas voltam ao modelo como observações;
- Actions não marcadas como `agent_exposed` nunca aparecem para o modelo.

`system.run_command`, por exemplo, existe para fluxos controlados, mas não é exposta ao agente autônomo por padrão.

## Percepção de tela

O Native Core entrega apenas uma captura BMP da tela principal. OCR é uma camada Python separada e opcional.

Instalação:

```bash
pip install -e ".[vision]"
```

O OCR retorna regiões estruturadas:

```json
{
  "text": "Configurações",
  "confidence": 0.96,
  "box": [[100, 200], [220, 200], [220, 240], [100, 240]],
  "center": {"x": 160, "y": 220}
}
```

A busca normaliza caixa, espaços e acentos antes de comparar textos, além de possuir comparação aproximada simples para tolerar pequenos erros do OCR.

## Segurança arquitetural

Existem três travas diferentes:

```text
Feature habilitada
        +
Plugin habilitado
        +
Permissão concedida
        ↓
Action disponível e executável
```

Uma capacidade existir no código não significa que o agente possa utilizá-la.

## Estado atual

A captura, mouse e teclado nativos estão implementados inicialmente para Windows. Codespaces/Linux continuam úteis para UI, protocolo de Actions e testes, mas não representam o ambiente gráfico Windows real.

O ponteiro atual ainda é o cursor normal do sistema operacional. Um ponteiro virtual independente é uma etapa futura e deverá ter backend próprio.
