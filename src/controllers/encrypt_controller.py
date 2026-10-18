from random import randint


class EncryptController:
    """Connects EncryptPage to the cipher.

    The output is recalculated live whenever the input text, the shift or the
    "use random shift" option changes. With the random option on, the shift
    widget is disabled and every recalculation picks a new shift.
    """

    MIN_RANDOM_SHIFT = 1
    MAX_RANDOM_SHIFT = 25

    def __init__(self, page, cipher):
        self.page = page
        self.cipher = cipher

        page.encrypt_input.textChanged.connect(self.update_output)
        page.shift_widget.value_changed.connect(self.update_output)
        page.random_checkbox.toggled.connect(self.on_random_toggled)
        page.encrypt_reset_button.clicked.connect(self.reset)

    def update_output(self):
        text = self.page.encrypt_input.toPlainText()
        result = self.cipher.caesar(text, self._current_shift())
        self.page.encrypt_output.setPlainText(result)

        has_result = bool(text and result)
        self.page.encrypt_reset_button.setEnabled(has_result)
        self.page.encrypt_copy_button.setEnabled(has_result)

    def on_random_toggled(self, checked):
        self.page.shift_widget.setDisabled(checked)
        self.update_output()

    def reset(self):
        self.page.encrypt_input.clear()
        self.page.shift_widget.reset()
        self.page.random_checkbox.setChecked(False)

    def _current_shift(self):
        if self.page.random_checkbox.isChecked():
            return randint(self.MIN_RANDOM_SHIFT, self.MAX_RANDOM_SHIFT)
        return self.page.shift_widget.value
