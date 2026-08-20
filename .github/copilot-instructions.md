# FreeCAD MCP Next repository instructions

- This repository contains two cooperating components: a FreeCAD workbench in the repository
  root (`Init.py`, `InitGui.py`, and `rpc_server/`) and a Python stdio MCP server in
  `src/freecad_mcp/`.
- Preserve the local-only security default. RPC must bind to localhost unless the user explicitly
  enables remote connections, and port `9875` must never be exposed publicly by default.
- FreeCAD document and GUI mutations must run sequentially on FreeCAD's GUI thread. Do not turn
  document-changing operations into parallel calls.
- Keep the version in `pyproject.toml` synchronized with the version and date in `package.xml`.
- Keep Python 3.12 compatibility for the MCP package and FreeCAD 1.0 compatibility for the addon.
- Do not import FreeCAD-only modules during ordinary unit-test collection. Mock the small FreeCAD
  surface required by tests.
- Preserve MIT attribution to `neka-nat/freecad-mcp` and Shirokuma (k tanaka) in `LICENSE` and
  `NOTICE.md`.
- User documentation must remain available in both Russian and English.
- Use Conventional Commit prefixes (`feat:`, `fix:`, `docs:`, `deps:`) so Release Please can
  calculate versions and generate changelogs.
- Do not create release tags manually during the normal release flow. Merge the Release Please PR.
- Run `uv sync --dev`, `uv run ruff check .`, `uv run ruff format --check .`, and
  `uv run pytest` before proposing a completed change.
- For release-affecting changes, also run `uv build`, `uv run twine check dist/*`, and
  `uv run python scripts/build_addon.py`.
- Do not commit generated files from `dist/`, `build/`, `build-check/`, virtual environments, logs,
  or local MCP configuration containing personal paths or secrets.
