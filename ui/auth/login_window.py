import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QCheckBox
from PyQt6.QtCore import Qt
from db import DB


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DB()
        self.setWindowTitle("Вход в систему")
        self.setGeometry(50, 50, 1125, 700)  
        self.center_window()  
        self.setup_ui()

    def center_window(self):
        screen = QApplication.primaryScreen().availableGeometry()
        window_geometry = self.frameGeometry()
        center_point = screen.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)


        exit_button = QPushButton("Выход")
        exit_button.setObjectName("ExitButton") 
        exit_button.clicked.connect(self.close) 

        top_layout = QHBoxLayout()
        top_layout.addStretch(1)
        top_layout.addWidget(exit_button)
        layout.addLayout(top_layout)

        login_label = QLabel("Логин")
        login_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.username_input = QLineEdit()
        self.username_input.setObjectName("LoginInput")

        password_label = QLabel("Пароль")
        password_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.password_input = QLineEdit()
        self.password_input.setObjectName("PasswordInput")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.show_password_checkbox = QCheckBox("Показать пароль")
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)

        login_button = QPushButton("Вход")
        login_button.setObjectName("LoginButton")
        login_button.clicked.connect(self.try_login)

        form_layout = QVBoxLayout()
        form_layout.addStretch(1)
        form_layout.addWidget(login_label, alignment=Qt.AlignmentFlag.AlignCenter)
        form_layout.addWidget(self.username_input, alignment=Qt.AlignmentFlag.AlignCenter)
        form_layout.addWidget(password_label, alignment=Qt.AlignmentFlag.AlignCenter)
        form_layout.addWidget(self.password_input, alignment=Qt.AlignmentFlag.AlignCenter)
        form_layout.addWidget(self.show_password_checkbox, alignment=Qt.AlignmentFlag.AlignCenter)
        form_layout.addWidget(login_button, alignment=Qt.AlignmentFlag.AlignCenter)
        form_layout.addStretch(1)

        layout.addLayout(form_layout)
        layout.addStretch(1) 
        self.apply_login_styles()

    def apply_login_styles(self):

        login_styles = """
            QLabel {
                color: #000000;
                font-size: 24px;
                font-weight: bold;
            }
            QLineEdit {
                border: 3px solid #CCCCCC;
                border-radius: 12px;
                padding: 20px;
                font-size: 20px;
                background-color: #FFFFFF;
                color: #000000; /* Черный текст */
            }
            QPushButton {
                background-color: #FFFFFF;
                color: #000000;
                border: 3px solid #CCCCCC;
                border-radius: 12px;
                padding: 25px 20px;
                font-size: 24px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #F0F0F0;
            }
            QCheckBox {
                color: #000000;
                font-size: 24px;
            }
        """
        self.setStyleSheet(login_styles)

    def try_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        user = self.db.authenticate_user(username, password)

        if user:
            from ui.main_window import MainWindow
            self.main = MainWindow(username=user['username'], role=user['role'])
            self.main.show()
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка входа", "Неверное имя пользователя или пароль")

    def toggle_password_visibility(self, state):
        if state == Qt.CheckState.Checked.value:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
