class DecryptController:
    """Connects DecryptPage to the cipher.

    The output is recalculated live whenever the input text or the shift changes.

    The "use manual shift" checkbox is not wired yet: what it should do when
    unchecked (e.g. guess the shift automatically) has not been decided.
    """

    def __init__(self, page, cipher):
        self.page = page
        self.cipher = cipher

        page.decrypt_input.textChanged.connect(self.update_output)
        page.shift_widget.value_changed.connect(self.update_output)
        page.decrypt_reset_button.clicked.connect(self.reset)

    def update_output(self):
        text = self.page.decrypt_input.toPlainText()
        result = self.cipher.caesar(text, self.page.shift_widget.value)
        self.page.decrypt_output.setPlainText(result)

        has_result = bool(text and result)
        self.page.decrypt_reset_button.setEnabled(has_result)
        self.page.decrypt_copy_button.setEnabled(has_result)

    def reset(self):
        self.page.decrypt_input.clear()
        self.page.shift_widget.reset()
