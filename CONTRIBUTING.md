# Contributing

Python 3.12+ and `uv` are required for development.

```bash
uv sync --dev
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv run python scripts/build_addon.py
uv build
```

Keep FreeCAD-dependent imports out of unit-test collection, or provide a small fake
`FreeCAD` module in the test. Test the workbench manually in the oldest and newest
supported FreeCAD releases before publishing a tag.

Version updates must be applied to both `pyproject.toml` and `package.xml`; CI verifies
that they match. Release Please normally performs both updates automatically.

Use Conventional Commit prefixes for commits merged to `main`:

- `fix:` creates a patch release;
- `feat:` creates a minor release;
- `feat!:` or a `BREAKING CHANGE:` footer creates a major release;
- `docs:` and `deps:` are included in the generated changelog.

Release tags are not created manually during the normal workflow. Merge the automatically
maintained Release Please PR when its proposed version and changelog are ready.
