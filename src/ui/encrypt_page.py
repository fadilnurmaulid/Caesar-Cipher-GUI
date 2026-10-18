from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QSizePolicy, QWidget, QTextEdit, QCheckBox)

from src.ui.components import CopyrightLabel, ShiftWidget
from src.utils.clipboard import copy

class EncryptPage(QWidget):
    back_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setObjectName("encrypt_page")

        layout = QVBoxLayout()
        hbox0 = QHBoxLayout()
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()

        # layout widget
        self.encrypt_input = QTextEdit()
        self.encrypt_input.setPlaceholderText("Enter text to encrypt...")
        self.encrypt_input.setObjectName("txt_input")

        self.encrypt_output = QTextEdit()
        self.encrypt_output.setPlaceholderText("Encrypted result will appear here")
        self.encrypt_output.setReadOnly(True)
        self.encrypt_output.setObjectName("txt_output")

        # hbox0 widget
        self.back_button = QPushButton("\u2B05")
        self.back_button.setObjectName("back_btn")

        title_label = QLabel("Caesar Cipher: Encrypt")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        title_label.setObjectName("title_lbl")

        # hbox1 widget
        self.shift_widget = ShiftWidget()
        spacing_label = CopyrightLabel()

        self.random_checkbox = QCheckBox("use random shift")
        self.random_checkbox.setObjectName("random_cbx")

        # hbox2 widget
        self.encrypt_reset_button = QPushButton("\U0001F501 Reset")
        self.encrypt_reset_button.setDisabled(True)   
        self.encrypt_reset_button.setObjectName("reset_btn")

        self.encrypt_copy_button = QPushButton("\U0001F4CB Copy")
        self.encrypt_copy_button.setDisabled(True)
        self.encrypt_copy_button.setObjectName("copy_btn")
        self.encrypt_copy_button.setProperty("copied", False)

        # handle wiring (cipher logic is wired in EncryptController)
        self.back_button.clicked.connect(self.back_requested.emit)
        self.encrypt_copy_button.clicked.connect(lambda: copy(self.encrypt_output, self.encrypt_copy_button))

        # add widgets to layout
        hbox0.addWidget(self.back_button)
        hbox0.addWidget(title_label)

        hbox1.addWidget(self.shift_widget)
        hbox1.addWidget(spacing_label)
        hbox1.addWidget(self.random_checkbox)

        hbox2.addWidget(self.encrypt_reset_button)
        hbox2.addWidget(self.encrypt_copy_button)
        
        layout.addLayout(hbox0)
        layout.addWidget(self.encrypt_input)
        layout.addLayout(hbox1)
        layout.addLayout(hbox2)
        layout.addWidget(self.encrypt_output)
        self.setLayout(layout)
