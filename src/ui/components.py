from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QSizePolicy, QWidget


class ShiftWidget(QWidget):
    """Shift selector shared by the encrypt and decrypt pages: "Shift: [-] 00 [+]".

    A click changes the value by one step and holding a button repeats the step.
    The value stays within MIN_SHIFT..MAX_SHIFT: "-" stops at the minimum, while
    "+" wraps from the maximum back to the minimum.
    """

    value_changed = pyqtSignal(int)

    MIN_SHIFT = 0
    MAX_SHIFT = 26
    HOLD_INTERVAL_MS = 150

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("shift_widget")

        self._value = self.MIN_SHIFT
        self._held_step = 0
        self._hold_timer = QTimer(self)
        self._hold_timer.timeout.connect(self._repeat_held_step)

        self.shift_label = QLabel("Shift:")
        self.minus_button = QPushButton("-")
        self.value_label = QLabel(f"{self._value:02}")
        self.plus_button = QPushButton("+")

        # handle wiring (click = one step, press and hold = repeated steps)
        self.minus_button.clicked.connect(lambda: self._step(-1))
        self.minus_button.pressed.connect(lambda: self._start_hold(-1))
        self.minus_button.released.connect(self._hold_timer.stop)
        self.plus_button.clicked.connect(lambda: self._step(1))
        self.plus_button.pressed.connect(lambda: self._start_hold(1))
        self.plus_button.released.connect(self._hold_timer.stop)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.shift_label)
        layout.addWidget(self.minus_button)
        layout.addWidget(self.value_label)
        layout.addWidget(self.plus_button)

    @property
    def value(self):
        return self._value

    def set_value(self, value):
        value = max(self.MIN_SHIFT, min(self.MAX_SHIFT, value))
        if value == self._value:
            return
        self._value = value
        self.value_label.setText(f"{value:02}")
        self.value_changed.emit(value)

    def reset(self):
        self.set_value(self.MIN_SHIFT)

    def _step(self, direction):
        if direction < 0:
            self.set_value(self._value - 1)
        else:
            self.set_value((self._value + 1) % (self.MAX_SHIFT + 1))

    def _start_hold(self, direction):
        self._held_step = direction
        self._hold_timer.start(self.HOLD_INTERVAL_MS)

    def _repeat_held_step(self):
        if not self.isEnabled():
            self._hold_timer.stop()
            return
        self._step(self._held_step)


class CopyrightLabel(QLabel):
    """Small centered credit line shown between the shift selector and the options."""

    TEXT = "\u00A9 2025 Fadil Nurmaulid"

    def __init__(self, parent=None):
        super().__init__(self.TEXT, parent)
        self.setObjectName("copyright_lbl")
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
