# Continue, Ollama, and terminal clients

## Component roles

| Component | Role |
| --- | --- |
| FreeCAD + MCP Addon | Executes CAD commands and exposes the model view over XML-RPC at `127.0.0.1:9875` |
| `freecad-mcp` | Maps 14 MCP tools to FreeCAD RPC calls |
| Ollama | Runs the language model locally |
| Continue IDE/CLI, Codex, or another MCP client | Gives the model access to tools and starts `freecad-mcp` over stdio |

Ollama does not connect to FreeCAD directly. The integration needs an agent client that supports
both MCP and tool calling. Continue exposes MCP tools only in **Agent mode**.

## Continue + Ollama

### 1. Prepare Ollama

Make sure the service is available and pull a tool-capable model:

```powershell
ollama serve
ollama pull qwen3-coder:30b
ollama list
```

The Ollama Windows application often already serves `localhost:11434`, so a second
`ollama serve` is unnecessary. `qwen3-coder:30b` is an example rather than a requirement.
Another model is fine, but it must genuinely support tool calls for Agent mode.

### 2. Install and start the FreeCAD side

```powershell
git clone https://github.com/Lumitorus/freecad-mcp-next.git
cd freecad-mcp-next
uv sync
uv run python scripts/install_addon.py
```

Restart FreeCAD, select **MCP Addon**, and click **Start RPC Server**.

### 3. Configure Continue

Copy [`examples/config/continue-ollama.yaml`](../examples/config/continue-ollama.yaml)
to `~/.continue/config.yaml`, or merge its `models` and `mcpServers` sections into your existing
configuration. Replace `C:\path\to\freecad-mcp-next` with the real path.

The minimum MCP section is:

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

Alternatively, create `.continue/mcpServers/freecad-mcp.yaml` in a workspace:

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

Reload Continue, enable **Agent mode**, and begin with a read-only prompt:

```text
List the documents currently open in FreeCAD. Do not modify anything.
```

Official references: [MCP in Continue](https://docs.continue.dev/customize/deep-dives/mcp),
[config.yaml reference](https://docs.continue.dev/reference), and the
[Ollama provider](https://docs.continue.dev/customize/model-providers/top-level/ollama).

## Continue from a terminal

Continue CLI uses the same configuration format:

```powershell
cn --config "C:\path\to\freecad-mcp-next\examples\config\continue-ollama.yaml"
```

Use Agent mode in the terminal session and begin with a read-only operation. The default CLI
configuration path is `~/.continue/config.yaml`.

## Codex from a terminal

```powershell
codex mcp add freecad -- uv --directory "C:\path\to\freecad-mcp-next" run freecad-mcp
codex mcp list
codex
```

Codex CLI, its IDE extension, and the desktop app share MCP configuration on a Codex host.

## Test without a language model

Check the connection to FreeCAD:

```powershell
uv run python scripts/doctor.py
```

Open MCP Inspector and call tools manually:

```powershell
npx -y @modelcontextprotocol/inspector uv --directory "C:\path\to\freecad-mcp-next" run freecad-mcp
```

In the local Inspector page, click **Connect**, open **Tools**, and call `list_documents` first.

## Why `uv run freecad-mcp` appears to hang

It is an stdio protocol server, not an interactive shell. It waits for MCP JSON-RPC messages on
stdin, so displaying no prompt is expected. Stop it with `Ctrl+C`.

## Other clients

Any client that can spawn a local stdio MCP server can use this project. Configure:

```text
command: uv
args: --directory <repository-path> run freecad-mcp
transport: stdio
```

A client that supports only remote HTTP/SSE MCP needs a separate local stdio-to-HTTP gateway.
Continue, Codex, Copilot, Cursor, Cline, and most desktop clients do not need such a gateway.

## Local-model limitations

- The model must support tool calling or Continue will not expose tools in Agent mode.
- Smaller models may choose the wrong tool or generate invalid FreeCAD properties.
- Begin with read operations such as `list_documents` and `get_objects`, and save the FCStd file
  before allowing changes.
- Send FreeCAD modifications sequentially; its GUI and some FEM operations are not designed for
  parallel document mutation.
- Never expose RPC port `9875` to the public internet.

