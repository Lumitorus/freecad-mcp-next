# Continue, Ollama и терминальные клиенты

## Как разделены роли

| Компонент | Роль |
| --- | --- |
| FreeCAD + MCP Addon | Выполняет CAD-команды и отдаёт вид модели через XML-RPC `127.0.0.1:9875` |
| `freecad-mcp` | Преобразует 14 MCP-инструментов в вызовы FreeCAD |
| Ollama | Локально запускает языковую модель |
| Continue IDE/CLI, Codex или другой MCP-клиент | Передаёт модели инструменты и запускает `freecad-mcp` по stdio |

Ollama не подключается к FreeCAD напрямую. Для связки нужен агентный клиент, который
поддерживает MCP и tool calling. В Continue MCP работает только в **Agent mode**.

## Continue + Ollama

### 1. Подготовить Ollama

Убедитесь, что сервис запущен, затем скачайте модель с поддержкой tool calling:

```powershell
ollama serve
ollama pull qwen3-coder:30b
ollama list
```

На Windows приложение Ollama часто уже держит сервис на `localhost:11434`; тогда второй
`ollama serve` запускать не нужно. `qwen3-coder:30b` — пример, а не обязательная модель.
Можно выбрать другую, но для Agent mode ей нужна реальная поддержка вызова инструментов.

### 2. Установить и запустить FreeCAD-часть

```powershell
git clone https://github.com/Lumitorus/freecad-mcp-next.git
cd freecad-mcp-next
uv sync
uv run python scripts/install_addon.py
```

Перезапустите FreeCAD, выберите **MCP Addon** и нажмите **Start RPC Server**.

### 3. Настроить Continue

Скопируйте
[`examples/config/continue-ollama.yaml`](../examples/config/continue-ollama.yaml)
в `~/.continue/config.yaml` или объедините его секции `models` и `mcpServers` со своим
существующим конфигом. Замените путь `C:\path\to\freecad-mcp-next`.

Минимальная часть MCP:

```yaml
mcpServers:
  - name: FreeCAD MCP
    command: uv
    args:
      - --directory
      - C:\path\to\freecad-mcp-next
      - run
      - freecad-mcp
    connectionTimeout: 10000
```

Альтернативно создайте в проекте файл `.continue/mcpServers/freecad-mcp.yaml`:

```yaml
name: FreeCAD MCP
version: 1.0.0
schema: v1
mcpServers:
  - name: FreeCAD MCP
    command: uv
    args:
      - --directory
      - C:\path\to\freecad-mcp-next
      - run
      - freecad-mcp
```

Перезагрузите конфигурацию Continue, включите **Agent mode** и проверьте запросом:

```text
Покажи список открытых документов FreeCAD. Ничего не изменяй.
```

Только после успешного чтения переходите к изменяющим командам.

Официальные источники: [MCP в Continue](https://docs.continue.dev/customize/deep-dives/mcp),
[формат config.yaml](https://docs.continue.dev/reference),
[Ollama provider](https://docs.continue.dev/customize/model-providers/top-level/ollama).

## Continue из терминала

Continue CLI использует тот же формат конфигурации:

```powershell
cn --config "C:\path\to\freecad-mcp-next\examples\config\continue-ollama.yaml"
```

В интерактивном терминале выберите Agent mode и дайте сначала безопасный запрос на чтение.
Конфигурация CLI по умолчанию находится в `~/.continue/config.yaml`.

## Codex из терминала

```powershell
codex mcp add freecad -- uv --directory "C:\path\to\freecad-mcp-next" run freecad-mcp
codex mcp list
codex
```

Codex CLI, IDE extension и desktop app используют общий MCP-конфиг одного Codex-хоста.

## Проверка без языковой модели

Проверить соединение с FreeCAD:

```powershell
uv run python scripts/doctor.py
```

Открыть MCP Inspector и вручную вызывать инструменты:

```powershell
npx -y @modelcontextprotocol/inspector uv --directory "C:\path\to\freecad-mcp-next" run freecad-mcp
```

Inspector откроет локальную веб-панель. Нажмите **Connect**, перейдите в **Tools** и сначала
вызовите `list_documents`.

## Почему `uv run freecad-mcp` выглядит зависшим

Это stdio-сервер, а не интерактивная консоль. После запуска он ожидает MCP JSON-RPC во входном
потоке. Отсутствие приглашения командной строки — нормальное поведение; остановить процесс можно
через `Ctrl+C`.

## Совместимость с другими клиентами

Подойдёт любой клиент, который умеет запускать локальный stdio MCP-сервер. В его настройках
нужно передать три значения:

```text
command: uv
args: --directory <путь-к-репозиторию> run freecad-mcp
transport: stdio
```

Если клиент поддерживает только удалённый HTTP/SSE MCP, текущая версия напрямую не подойдёт:
понадобится отдельный локальный stdio-to-HTTP шлюз. Для Continue, Codex, Copilot, Cursor,
Cline и большинства desktop-клиентов шлюз не нужен.

## Ограничения локальных моделей

- Модель должна поддерживать tool calling, иначе инструменты не появятся в Agent mode.
- Маленькая модель может выбирать неправильный инструмент или генерировать неверные свойства.
- Начинайте с чтения (`list_documents`, `get_objects`) и сохраняйте FCStd перед изменениями.
- Запросы к FreeCAD выполняйте последовательно: GUI и часть FEM-операций не рассчитаны на
  параллельные изменения документа.
- Не открывайте RPC-порт `9875` в интернет.

