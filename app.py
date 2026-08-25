import sys

from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtWidgets import QApplication
from src.ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Caesar Cipher GUI")
    app.setOrganizationName("FCORTEX")

    # Custom Font
    font_path = "assets/fonts/FiraCode-Bold.ttf"
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id == -1:
        raise RuntimeError(f"Failed to load font: {font_path}")
    families = QFontDatabase.applicationFontFamilies(font_id)
    if not families:
        raise RuntimeError(f"No font family found: {font_path}")
    my_font = QFont(families[0])
    app.setFont(my_font)

    # Styles
    style_path = "src/styles/style.qss"
    with open(style_path, 'r', encoding="utf-8") as f:
        app.setStyleSheet(f.read())
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
