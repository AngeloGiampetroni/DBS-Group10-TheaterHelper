"""Sidebar page: runs the shared Chatbot implementation in `src/pages/chatbot.py`."""

from pathlib import Path
import runpy

_chatbot = Path(__file__).resolve().parent.parent / "chatbot.py"
runpy.run_path(str(_chatbot), run_name="__main__")
