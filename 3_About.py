"""Sidebar page: runs the shared About implementation in `src/pages/about.py`."""

from pathlib import Path
import runpy

_about = Path(__file__).resolve().parent.parent / "about.py"
runpy.run_path(str(_about), run_name="__main__")
