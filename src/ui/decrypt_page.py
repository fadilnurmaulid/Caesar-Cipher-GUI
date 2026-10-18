from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QSizePolicy, QWidget, QTextEdit, QCheckBox)

from src.ui.components import CopyrightLabel, ShiftWidget
from src.utils.clipboard import copy

class DecryptPage(QWidget):
    back_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setObjectName("decrypt_page")

        layout = QVBoxLayout()
        hbox0 = QHBoxLayout()
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()

        # layout widget
        self.decrypt_input = QTextEdit()
        self.decrypt_input.setPlaceholderText("Enter text to decrypt...")
        self.decrypt_input.setObjectName("txt_input")
        
        self.decrypt_output = QTextEdit()
        self.decrypt_output.setPlaceholderText("Decrypted result will appear here")
        self.decrypt_output.setReadOnly(True)
        self.decrypt_output.setObjectName("txt_output")

        # hbox0 widget
        self.back_button = QPushButton("\u2B05")
        self.back_button.setObjectName("back_btn")

        title_label = QLabel("Caesar Cipher: Decrypt")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        title_label.setObjectName("title_lbl")

        # hbox1 widget
        self.shift_widget = ShiftWidget()
        spacing_label = CopyrightLabel()

        self.manual_checkbox = QCheckBox("use manual shift")
        self.manual_checkbox.setObjectName("manual_cbx")

        # hbox2 widget
        self.decrypt_reset_button = QPushButton("\U0001F501 Reset")
        self.decrypt_reset_button.setDisabled(True)
        self.decrypt_reset_button.setObjectName("reset_btn")

        self.decrypt_copy_button = QPushButton("\U0001F4CB Copy")
        self.decrypt_copy_button.setDisabled(True)
        self.decrypt_copy_button.setObjectName("copy_btn")
        self.decrypt_copy_button.setProperty("copied", False)

        # handle wiring (cipher logic is wired in DecryptController)
        self.back_button.clicked.connect(self.back_requested.emit)
        self.decrypt_copy_button.clicked.connect(lambda: copy(self.decrypt_output, self.decrypt_copy_button))

        # add widgets to layouts
        hbox0.addWidget(self.back_button)
        hbox0.addWidget(title_label)

        hbox1.addWidget(self.shift_widget)
        hbox1.addWidget(spacing_label)
        hbox1.addWidget(self.manual_checkbox)

        hbox2.addWidget(self.decrypt_reset_button)
        hbox2.addWidget(self.decrypt_copy_button)

        layout.addLayout(hbox0)
        layout.addWidget(self.decrypt_input)
        layout.addLayout(hbox1)
        layout.addLayout(hbox2)
        layout.addWidget(self.decrypt_output)
        self.setLayout(layout)
