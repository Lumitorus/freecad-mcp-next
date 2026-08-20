from __future__ import annotations

from pathlib import Path

from scripts.install_addon import install

ROOT = Path(__file__).resolve().parents[1]


def test_installer_creates_expected_layout(tmp_path: Path) -> None:
    target, backup = install(ROOT, tmp_path)

    assert backup is None
    assert (target / "InitGui.py").is_file()
    assert (target / "rpc_server" / "rpc_server.py").is_file()


def test_installer_preserves_previous_installation(tmp_path: Path) -> None:
    target, _ = install(ROOT, tmp_path)
    marker = target / "old-version.txt"
    marker.write_text("keep me", encoding="utf-8")

    _, backup = install(ROOT, tmp_path)

    assert backup is not None
    assert (backup / "old-version.txt").read_text(encoding="utf-8") == "keep me"
