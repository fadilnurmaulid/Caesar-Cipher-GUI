from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QWidget, QTextEdit

class DecryptPage(QWidget):
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
        self.decrypt_shift_label = QLabel("Shift:")
        self.decrypt_shift_label.setObjectName("shift_lbl")

        self.minus_button_decrypt = QPushButton("-")
        self.minus_button_decrypt.setObjectName("minus_btn")

        self.shift_decrypt_value_label = QLabel("00")
        self.shift_decrypt_value_label.setObjectName("shift_value_lbl")

        self.plus_button_decrypt = QPushButton("+")
        self.plus_button_decrypt.setObjectName("plus_btn")

        spacing_label = QLabel("\u00A9 2025 Fadil Nurmaulid")
        spacing_label.setStyleSheet("font-size: 8pt")
        spacing_label.setAlignment(Qt.AlignCenter)
        spacing_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # hbox2 widget
        self.decrypt_reset_button = QPushButton("\U0001F501 Reset")
        self.decrypt_reset_button.setDisabled(True)
        self.decrypt_reset_button.setObjectName("reset_btn")

        self.decrypt_copy_button = QPushButton("\U0001F4CB Copy")
        self.decrypt_copy_button.setDisabled(True)
        self.decrypt_copy_button.setObjectName("copy_btn")

        # add widgets to layouts
        hbox0.addWidget(self.back_button)
        hbox0.addWidget(title_label)

        hbox1.addSpacing(10)
        hbox1.addWidget(self.decrypt_shift_label)
        hbox1.addWidget(self.minus_button_decrypt)
        hbox1.addWidget(self.shift_decrypt_value_label)
        hbox1.addWidget(self.plus_button_decrypt)
        hbox1.addWidget(spacing_label)

        hbox2.addSpacing(10)
        hbox2.addWidget(self.decrypt_reset_button)
        hbox2.addWidget(self.decrypt_copy_button)
        hbox2.addSpacing(10)

        layout.addLayout(hbox0)
        layout.addWidget(self.decrypt_input)
        layout.addLayout(hbox1)
        layout.addLayout(hbox2)
        layout.addWidget(self.decrypt_output)
        self.setLayout(layout)