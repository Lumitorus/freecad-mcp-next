#!/usr/bin/env python3
"""Install the repository's FreeCAD workbench into the user Mod directory."""

from __future__ import annotations

import argparse
import os
import platform
import shutil
import sys
from datetime import datetime
from pathlib import Path

ADDON_FILES = ("Init.py", "InitGui.py", "package.xml", "LICENSE")


def default_user_data_dir() -> Path:
    system = platform.system()
    if system == "Windows":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming")) / "FreeCAD"
    elif system == "Darwin":
        base = Path.home() / "Library" / "Preferences" / "FreeCAD"
    else:
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share")) / "FreeCAD"

    versioned = sorted(
        (path for path in base.glob("v*-*") if path.is_dir()),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    return versioned[0] if versioned else base


def install(source: Path, user_data_dir: Path) -> tuple[Path, Path | None]:
    missing = [name for name in ADDON_FILES if not (source / name).is_file()]
    if not (source / "rpc_server").is_dir():
        missing.append("rpc_server/")
    if missing:
        raise FileNotFoundError(f"Incomplete source tree; missing: {', '.join(missing)}")

    mod_dir = user_data_dir / "Mod"
    target = mod_dir / "FreeCADMCP"
    backup = None
    mod_dir.mkdir(parents=True, exist_ok=True)

    if target.exists():
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        backup = target.with_name(f"FreeCADMCP.backup-{stamp}")
        target.rename(backup)

    try:
        target.mkdir()
        for name in ADDON_FILES:
            shutil.copy2(source / name, target / name)
        shutil.copytree(source / "rpc_server", target / "rpc_server")
    except Exception:
        shutil.rmtree(target, ignore_errors=True)
        if backup is not None and backup.exists():
            backup.rename(target)
        raise
    return target, backup


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--user-data-dir",
        type=Path,
        help="Value printed by FreeCAD Python console: App.getUserAppDataDir()",
    )
    args = parser.parse_args()

    source = Path(__file__).resolve().parents[1]
    user_data_dir = (args.user_data_dir or default_user_data_dir()).expanduser().resolve()
    target, backup = install(source, user_data_dir)
    print(f"Installed FreeCAD MCP workbench to: {target}")
    if backup:
        print(f"Previous installation preserved at: {backup}")
    print("Restart FreeCAD, select 'MCP Addon', then click 'Start RPC Server'.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
