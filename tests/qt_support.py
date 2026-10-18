"""Shared setup for GUI tests: a headless QApplication with the real font and stylesheet."""
import os

# Never open real windows while testing.
os.environ["QT_QPA_PLATFORM"] = "offscreen"

from PyQt5.QtWidgets import QApplication

from app import load_font, load_styles

_app = None


def get_app():
    global _app
    if _app is None:
        _app = QApplication.instance() or QApplication([])
        load_font(_app)
        load_styles(_app)
    return _app
