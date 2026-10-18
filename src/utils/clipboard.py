from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication

COPIED_FLASH_MS = 1000


def copy(text_edit, button):
    """Copy the text edit's content to the clipboard and flash "Copied!" on the button."""
    QApplication.clipboard().setText(text_edit.toPlainText())
    _set_copied(button, True)
    button.setDisabled(True)
    button.setText("✅Copied!")
    QTimer.singleShot(COPIED_FLASH_MS, lambda: _restore_copy_button(text_edit, button))


def _set_copied(button, copied):
    button.setProperty("copied", copied)
    # Qt does not re-evaluate the [copied="..."] selector in style.qss after a
    # property change, so the style has to be refreshed by hand.
    button.style().unpolish(button)
    button.style().polish(button)


def _restore_copy_button(text_edit, button):
    _set_copied(button, False)
    # Stay disabled if the content was cleared (e.g. by Reset) while "Copied!" was showing.
    button.setEnabled(bool(text_edit.toPlainText()))
    button.setText("\U0001F4CB Copy")
