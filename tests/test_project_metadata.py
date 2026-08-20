from __future__ import annotations

import json
import tomllib
import zipfile
from pathlib import Path
from xml.etree import ElementTree

from scripts.build_addon import build

ROOT = Path(__file__).resolve().parents[1]


def test_python_and_addon_versions_match() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    package = ElementTree.parse(ROOT / "package.xml").getroot()

    assert package.findtext("{*}version") == pyproject["project"]["version"]


def test_required_addon_metadata_exists() -> None:
    package = ElementTree.parse(ROOT / "package.xml").getroot()

    assert package.findtext("{*}name") == "FreeCAD MCP"
    assert package.findtext("{*}maintainer") == "Lumitorus"
    assert package.findtext("{*}url") == "https://github.com/Lumitorus/freecad-mcp-next"
    assert package.findtext(".//{*}classname") == "FreeCADMCPAddonWorkbench"
    assert package.findtext(".//{*}subdirectory") == "./"


def test_addon_archive_has_expected_layout(tmp_path: Path, monkeypatch) -> None:
    import scripts.build_addon as builder

    monkeypatch.setattr(builder, "DIST", tmp_path)
    archive = build()

    with zipfile.ZipFile(archive) as bundle:
        names = set(bundle.namelist())

    assert "FreeCADMCP/InitGui.py" in names
    assert "FreeCADMCP/package.xml" in names
    assert "FreeCADMCP/rpc_server/rpc_server.py" in names
    assert archive.with_suffix(".zip.sha256").is_file()


def test_continue_ollama_example_is_valid() -> None:
    import yaml

    config = yaml.safe_load(
        (ROOT / "examples" / "config" / "continue-ollama.yaml").read_text(encoding="utf-8")
    )

    assert config["schema"] == "v1"
    assert config["models"][0]["provider"] == "ollama"
    assert config["mcpServers"][0]["command"] == "uv"
    assert config["mcpServers"][0]["args"][-1] == "freecad-mcp"


def test_release_please_updates_both_version_files() -> None:
    config = json.loads((ROOT / "release-please-config.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / ".release-please-manifest.json").read_text(encoding="utf-8"))
    package = (ROOT / "package.xml").read_text(encoding="utf-8")

    project = config["packages"]["."]
    assert project["release-type"] == "python"
    assert {item["path"] for item in project["extra-files"]} == {"package.xml"}
    assert "x-release-please-version" in package

    version = manifest["."]
    version_parts = version.split(".")
    assert len(version_parts) == 3
    assert all(part.isdigit() for part in version_parts)

    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    assert any(heading in changelog for heading in (f"## [{version}]", f"## {version}"))
