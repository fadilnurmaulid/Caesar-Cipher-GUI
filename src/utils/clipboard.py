from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication

def copy(text_edit, button):
        text = text_edit.toPlainText()
        QApplication.clipboard().setText(text)
        button.setProperty("copied", True)
        button.setDisabled(True)      
        button.setText("✅Copied!")
        QTimer.singleShot(1000, lambda: reset_button(button))

def reset_button(button):
    button.setProperty("copied", False)
    button.setDisabled(False)
    button.setText("\U0001F4CB Copy")