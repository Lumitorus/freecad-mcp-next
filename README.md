# FreeCAD MCP Next

[Русский](#русский) · [English](#english)

## Русский

FreeCAD MCP Next связывает FreeCAD с MCP-клиентами: Codex, GitHub Copilot Chat
в Visual Studio Code и другими совместимыми ассистентами.

Проект состоит из двух локальных процессов:

1. Workbench внутри FreeCAD открывает XML-RPC на `127.0.0.1:9875`.
2. Команда `freecad-mcp` работает как stdio MCP-сервер для AI-клиента.

### Быстрый старт из исходников

Требования: FreeCAD 1.0 или новее, Python 3.12+, Git и
[`uv`](https://docs.astral.sh/uv/).

```powershell
git clone https://github.com/Lumitorus/freecad-mcp-next.git
cd freecad-mcp-next
uv sync
uv run python scripts/install_addon.py
```

Перезапустите FreeCAD, выберите рабочее окружение **MCP Addon** и нажмите
**Start RPC Server**. Затем подключите MCP-клиент:

```powershell
codex mcp add freecad -- uv --directory "C:\path\to\freecad-mcp-next" run freecad-mcp
```

Для Copilot скопируйте [`.vscode/mcp.example.json`](.vscode/mcp.example.json) в
`.vscode/mcp.json`, замените путь и выполните в VS Code команду **MCP: List Servers**.

Полная инструкция: [docs/installation.ru.md](docs/installation.ru.md).

Отдельная благодарность
[`neka-nat/freecad-mcp`](https://github.com/neka-nat/freecad-mcp) за основу проекта.

## English

FreeCAD MCP Next connects FreeCAD to MCP clients such as Codex, GitHub Copilot
Chat in Visual Studio Code, and other compatible assistants.

The project uses two local processes:

1. A FreeCAD workbench exposes XML-RPC on `127.0.0.1:9875`.
2. The `freecad-mcp` command provides an stdio MCP server to the AI client.

### Quick start from source

Requirements: FreeCAD 1.0 or newer, Python 3.12+, Git, and
[`uv`](https://docs.astral.sh/uv/).

```powershell
git clone https://github.com/Lumitorus/freecad-mcp-next.git
cd freecad-mcp-next
uv sync
uv run python scripts/install_addon.py
```

Restart FreeCAD, select the **MCP Addon** workbench, and click
**Start RPC Server**. Then connect your MCP client:

```powershell
codex mcp add freecad -- uv --directory "C:\path\to\freecad-mcp-next" run freecad-mcp
```

For Copilot, copy [`.vscode/mcp.example.json`](.vscode/mcp.example.json) to
`.vscode/mcp.json`, replace the path, and run **MCP: List Servers** in VS Code.

Full guide: [docs/installation.en.md](docs/installation.en.md).

Special thanks to
[`neka-nat/freecad-mcp`](https://github.com/neka-nat/freecad-mcp) for providing
the foundation of this project.

## Development and releases

Pull requests run linting, unit tests, package builds, and addon validation on
Windows, macOS, and Linux. A `v*` tag creates:

- a Python wheel and source distribution;
- `FreeCADMCP-<version>.zip` for manual FreeCAD installation;
- SHA-256 checksum files;
- a GitHub Release containing all artifacts.

See [CONTRIBUTING.md](CONTRIBUTING.md) and [docs/releasing.md](docs/releasing.md).

## Continue, Ollama, and terminal clients

Ollama provides the local language model; Continue acts as the MCP client and
connects that model to FreeCAD tools. A ready-to-copy configuration is available
at [examples/config/continue-ollama.yaml](examples/config/continue-ollama.yaml).

Detailed Russian and English instructions:

- [docs/clients.ru.md](docs/clients.ru.md)
- [docs/clients.en.md](docs/clients.en.md)

## License and acknowledgements

Maintained by [Lumitorus](https://github.com/Lumitorus) and distributed under
the MIT License.

Special thanks to
[`neka-nat/freecad-mcp`](https://github.com/neka-nat/freecad-mcp) for the
foundation of this project. See [NOTICE.md](NOTICE.md).
