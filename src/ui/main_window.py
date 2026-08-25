from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStackedWidget, QVBoxLayout, QWidget

from src.ui.home_page import HomePage
from src.ui.encrypt_page import EncryptPage
from src.ui.decrypt_page import DecryptPage

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Caesar Cipher")
        self.resize(700, 400)
        self.setMinimumSize(700, 400)

        # Custom Window Icon
        icon_path = "assets/icons/Icon.ico"
        self.setWindowIcon(QIcon(icon_path))

        # Initiate Page Interface
        self.home_page = HomePage()
        self.encrypt_page = EncryptPage()
        self.decrypt_page = DecryptPage()

        # Creating QStackedWidget and Adding Pages
        self.pages = QStackedWidget()
        self.pages.addWidget(self.home_page)    # Index 0
        self.pages.addWidget(self.encrypt_page) # Index 1
        self.pages.addWidget(self.decrypt_page) # Index 2

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.pages)
        self.setLayout(main_layout)

    def show_home(self):
        self.pages.setCurrentWidget(self.home_page)

    def show_encrypt(self):
        self.pages.setCurrentWidget(self.encrypt_page)

    def show_decrypt(self):
        self.pages.setCurrentWidget(self.decrypt_page)
