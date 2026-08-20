#!/usr/bin/env python3
"""Build a deterministic FreeCAD addon ZIP from the repository root."""

from __future__ import annotations

import hashlib
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
ADDON_FILES = ("Init.py", "InitGui.py", "package.xml", "LICENSE", "NOTICE.md")


def package_version() -> str:
    root = ElementTree.parse(ROOT / "package.xml").getroot()
    version = root.find("{*}version")
    if version is None or not version.text:
        raise RuntimeError("package.xml does not contain a version")
    return version.text.strip()


def build() -> Path:
    version = package_version()
    DIST.mkdir(parents=True, exist_ok=True)
    archive = DIST / f"FreeCADMCP-{version}.zip"
    archive.unlink(missing_ok=True)
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        paths = [ROOT / name for name in ADDON_FILES]
        paths.extend(path for path in (ROOT / "rpc_server").rglob("*") if path.is_file())
        for path in sorted(paths):
            if "__pycache__" in path.parts or path.suffix in {".pyc", ".pyo"}:
                continue
            relative = path.relative_to(ROOT).as_posix()
            info = zipfile.ZipInfo(f"FreeCADMCP/{relative}", date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, path.read_bytes())

    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    archive.with_suffix(".zip.sha256").write_text(
        f"{digest}  {archive.name}\n", encoding="utf-8", newline="\n"
    )
    return archive


if __name__ == "__main__":
    result = build()
    print(result)
    sys.exit(0)
