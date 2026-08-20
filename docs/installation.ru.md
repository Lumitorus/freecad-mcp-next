# Установка FreeCAD MCP Next

## 1. Что устанавливается

FreeCAD MCP состоит из двух частей:

- **FreeCAD Workbench** — работает внутри FreeCAD и слушает локальный XML-RPC-порт `9875`;
- **MCP-сервер** — запускается Codex или VS Code по stdio и пересылает команды в FreeCAD.

Обе части нужны одновременно. Docker не требуется: для обычного настольного FreeCAD он
только усложняет доступ к GUI, пользовательскому профилю и локальному порту.

## 2. Требования

- Windows 10/11, macOS или Linux;
- FreeCAD 1.0 или новее;
- Python 3.12 или новее для MCP-сервера;
- Git;
- `uv` — менеджер Python-окружения и запускатель.

Проверка:

```text
FreeCAD: Справка → О FreeCAD
python --version
git --version
uv --version
```

## 3. Скачать проект

```bash
git clone https://github.com/Lumitorus/freecad-mcp-next.git
cd freecad-mcp-next
uv sync
```

До первой публикации на PyPI запускайте сервер из клона через `uv --directory ... run`.
После публикации пакета можно будет заменить это на
`uvx --from freecad-mcp-next freecad-mcp`.

## 4. Установить Workbench

### Автоматически из клона

```bash
uv run python scripts/install_addon.py
```

Скрипт сохраняет предыдущую установку рядом как `FreeCADMCP.backup-ДАТА-ВРЕМЯ`.

Если FreeCAD использует нестандартный профиль, откройте в FreeCAD меню
**Вид → Панели → Python console** и выполните:

```python
App.getUserAppDataDir()
```

Передайте выведенный путь явно:

```powershell
uv run python scripts/install_addon.py --user-data-dir "C:\Users\NAME\AppData\Roaming\FreeCAD\v1-1"
```

Для FreeCAD 1.1 в Windows важен именно версионный каталог вроде `v1-1`; установка только
в `%APPDATA%\FreeCAD\Mod` может быть невидимой для этого профиля.

### Вручную из Release ZIP

1. Скачайте `FreeCADMCP-<версия>.zip` из GitHub Releases.
2. Найдите пользовательский каталог командой `App.getUserAppDataDir()`.
3. Распакуйте архив так, чтобы существовал файл
   `<UserAppDataDir>/Mod/FreeCADMCP/InitGui.py`.
4. Полностью перезапустите FreeCAD.

### Через Addon Manager

После включения проекта в официальный индекс FreeCAD откройте
**Tools → Addon Manager**, найдите **FreeCAD MCP** и установите его. До включения в индекс
используйте ручной способ или пользовательский источник репозитория в настройках Addon Manager.

## 5. Запустить FreeCAD-часть

1. Перезапустите FreeCAD.
2. В списке рабочих окружений выберите **MCP Addon**.
3. Нажмите **Start RPC Server**.
4. Для автозапуска используйте **Toggle Auto Start**.

По умолчанию разрешён только localhost. Не включайте удалённые подключения и не открывайте
порт `9875` в интернет без отдельной защищённой сети.

Диагностика:

```bash
uv run python scripts/doctor.py
```

## 6. Подключить Codex

Самый простой вариант:

```powershell
codex mcp add freecad -- uv --directory "C:\path\to\freecad-mcp-next" run freecad-mcp
codex mcp list
```

Или добавьте в `%USERPROFILE%\.codex\config.toml` (Windows) либо
`~/.codex/config.toml` (macOS/Linux):

```toml
[mcp_servers.freecad]
command = "uv"
args = ["--directory", "C:\\path\\to\\freecad-mcp-next", "run", "freecad-mcp"]
```

На macOS/Linux используйте обычный путь:

```toml
[mcp_servers.freecad]
command = "uv"
args = ["--directory", "/home/name/freecad-mcp-next", "run", "freecad-mcp"]
```

Перезапустите Codex. FreeCAD должен быть открыт, а RPC-сервер — запущен.

## 7. Подключить GitHub Copilot Chat в VS Code

Требуется актуальный VS Code, расширение GitHub Copilot и доступ к Agent mode/MCP.

1. Скопируйте `.vscode/mcp.example.json` в `.vscode/mcp.json`.
2. Замените путь к репозиторию.
3. Откройте палитру команд и выполните **MCP: List Servers**.
4. Запустите сервер `freecad`, если он ещё не запущен.
5. Откройте Copilot Chat, переключитесь в **Agent** и разрешите использование инструментов.

Пример `.vscode/mcp.json` для Windows:

```json
{
  "servers": {
    "freecad": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "--directory",
        "C:\\path\\to\\freecad-mcp-next",
        "run",
        "freecad-mcp"
      ]
    }
  }
}
```

Не коммитьте `.vscode/mcp.json`, если в нём появились секреты или персональные пути.

## 8. Типовые проблемы

### Workbench не появился

- Проверьте путь через `App.getUserAppDataDir()`.
- Должен существовать ровно `Mod/FreeCADMCP/InitGui.py`, без лишнего уровня вложенности.
- Полностью закройте все экземпляры FreeCAD и запустите один заново.
- Откройте **Вид → Панели → Отчёт** и найдите ошибку импорта `FreeCADMCP`.

### MCP-клиент видит сервер, но инструменты падают

- Запустите **Start RPC Server** внутри FreeCAD.
- Выполните `uv run python scripts/doctor.py`.
- Проверьте, что другой экземпляр FreeCAD не занял порт `9875`.

### `uv` не найден из VS Code или Codex

Укажите абсолютный путь к `uv.exe`/`uv` в поле `command` либо перезапустите приложение
после изменения `PATH`.

Настройка Continue, Ollama, Continue CLI и MCP Inspector вынесена в
[отдельную инструкцию](clients.ru.md).
