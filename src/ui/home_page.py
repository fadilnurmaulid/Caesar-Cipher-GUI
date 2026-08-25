from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QWidget

class HomePage(QWidget):
    encrypt_requested = pyqtSignal()
    decrypt_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()

        self.setObjectName("home_page")

        layout = QVBoxLayout()
        hbox = QHBoxLayout()

        label = QLabel("CAESAR CIPHER")
        label.setAlignment(Qt.AlignCenter)

        self.encrypt_button = QPushButton("Encrypt")
        self.encrypt_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.encrypt_button.clicked.connect(self.encrypt_requested.emit)
                
        self.decrypt_button = QPushButton("Decrypt")
        self.decrypt_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.decrypt_button.clicked.connect(self.decrypt_requested.emit)
       
        hbox.addWidget(self.encrypt_button)
        hbox.addWidget(self.decrypt_button)
        layout.addWidget(label)
        layout.addLayout(hbox)
        self.setLayout(layout)