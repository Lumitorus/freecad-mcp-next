# Installing FreeCAD MCP Next

## 1. Components

FreeCAD MCP has two parts:

- the **FreeCAD workbench**, running inside FreeCAD and listening on local XML-RPC port `9875`;
- the **MCP server**, started over stdio by Codex or VS Code and forwarding calls to FreeCAD.

Both parts must run together. Docker is not required for normal desktop use because it adds
friction around the FreeCAD GUI, user profile, and host networking.

## 2. Requirements

- Windows 10/11, macOS, or Linux;
- FreeCAD 1.0 or newer;
- Python 3.12 or newer for the MCP server;
- Git;
- the `uv` Python environment and application runner.

## 3. Clone and prepare

```bash
git clone https://github.com/Lumitorus/freecad-mcp-next.git
cd freecad-mcp-next
uv sync
```

Until the first PyPI release, run the server from this clone with
`uv --directory ... run`. After publication, this can become
`uvx --from freecad-mcp-next freecad-mcp`.

## 4. Install the workbench

### Automatically from the clone

```bash
uv run python scripts/install_addon.py
```

The installer preserves an existing installation beside it as
`FreeCADMCP.backup-DATE-TIME`.

If FreeCAD uses a custom profile, open **View → Panels → Python console** and run:

```python
App.getUserAppDataDir()
```

Pass that exact path to the installer:

```powershell
uv run python scripts/install_addon.py --user-data-dir "C:\Users\NAME\AppData\Roaming\FreeCAD\v1-1"
```

FreeCAD 1.1 on Windows may use a versioned directory such as `v1-1`. Installing only to
`%APPDATA%\FreeCAD\Mod` can therefore leave the workbench invisible to that profile.

### Manually from a release ZIP

1. Download `FreeCADMCP-<version>.zip` from GitHub Releases.
2. Find the user directory with `App.getUserAppDataDir()`.
3. Extract the archive so that
   `<UserAppDataDir>/Mod/FreeCADMCP/InitGui.py` exists.
4. Restart FreeCAD completely.

### Addon Manager

After the project is accepted into the official FreeCAD addon index, open
**Tools → Addon Manager**, find **FreeCAD MCP**, and install it. Before that, use the
manual method or configure the repository as a custom Addon Manager source.

## 5. Start the FreeCAD side

1. Restart FreeCAD.
2. Select the **MCP Addon** workbench.
3. Click **Start RPC Server**.
4. Use **Toggle Auto Start** if the RPC service should start with FreeCAD.

Localhost is the secure default. Do not enable remote connections or expose port `9875`
to the public internet without a separately secured network layer.

Run the diagnostic check with:

```bash
uv run python scripts/doctor.py
```

## 6. Connect Codex

The CLI method is the shortest:

```powershell
codex mcp add freecad -- uv --directory "C:\path\to\freecad-mcp-next" run freecad-mcp
codex mcp list
```

Alternatively, add this to `%USERPROFILE%\.codex\config.toml` on Windows or
`~/.codex/config.toml` on macOS/Linux:

```toml
[mcp_servers.freecad]
command = "uv"
args = ["--directory", "C:\\path\\to\\freecad-mcp-next", "run", "freecad-mcp"]
```

Restart Codex afterward. FreeCAD must be open and its RPC server must be running.

## 7. Connect GitHub Copilot Chat in VS Code

Use a current VS Code release, the GitHub Copilot extension, and an account or organization
where Agent mode and MCP are enabled.

1. Copy `.vscode/mcp.example.json` to `.vscode/mcp.json`.
2. Replace the repository path.
3. Run **MCP: List Servers** from the Command Palette.
4. Start the `freecad` server if needed.
5. Open Copilot Chat, switch to **Agent**, and enable the server tools.

Windows example:

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

Do not commit `.vscode/mcp.json` if it later contains secrets or personal paths.

## 8. Troubleshooting

### The workbench is missing

- Verify the directory with `App.getUserAppDataDir()`.
- Ensure the path is exactly `Mod/FreeCADMCP/InitGui.py`, without an extra nested folder.
- Close every FreeCAD process, then start one instance.
- Open **View → Panels → Report view** and look for a `FreeCADMCP` import error.

### The MCP server starts but tool calls fail

- Click **Start RPC Server** inside FreeCAD.
- Run `uv run python scripts/doctor.py`.
- Check whether another FreeCAD instance already owns port `9875`.

### Codex or VS Code cannot find `uv`

Set `command` to the absolute path of `uv.exe`/`uv`, or restart the application after
changing `PATH`.

See the [client guide](clients.en.md) for Continue, Ollama, Continue CLI, and MCP Inspector.
