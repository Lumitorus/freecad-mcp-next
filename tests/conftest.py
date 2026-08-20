from __future__ import annotations

import sys
import types


class _Console:
    @staticmethod
    def PrintWarning(message: str) -> None:
        del message


fake_freecad = types.ModuleType("FreeCAD")
fake_freecad.Console = _Console()
sys.modules.setdefault("FreeCAD", fake_freecad)
