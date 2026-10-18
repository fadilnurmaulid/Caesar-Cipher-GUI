import sys

from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtWidgets import QApplication

from src.ui.main_window import MainWindow
from src.utils.resources import resource_path

def load_font(app):
    font_path = resource_path("assets/fonts/FiraCode-Bold.ttf")
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id == -1:
        raise RuntimeError(f"Failed to load font: {font_path}")
    families = QFontDatabase.applicationFontFamilies(font_id)
    if not families:
        raise RuntimeError(f"No font family found: {font_path}")
    app.setFont(QFont(families[0]))

def load_styles(app):
    style_path = resource_path("src/styles/style.qss")
    with open(style_path, 'r', encoding="utf-8") as f:
        app.setStyleSheet(f.read())

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Caesar Cipher GUI")
    app.setOrganizationName("FCORTEX")

    load_font(app)
    load_styles(app)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
