from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QGridLayout, QLineEdit, QMessageBox, QPushButton, QFormLayout
from PyQt6.QtCore import Qt, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator


class CustomerDialog(QDialog):
    def __init__(self, db, customer=None, parent=None):
        super().__init__(parent)
        self.db = db
        self.customer = customer
        self.setWindowTitle("Добавить клиента" if customer is None else "Изменить клиента")
        self.setGeometry(200, 200, 400, 250)
        self.center()

        main_layout = QVBoxLayout()

        if customer:
            id_layout = QHBoxLayout()
            id_layout.addWidget(QLabel("№:"))
            self.id_input = QLineEdit(str(customer['id']))
            self.id_input.setReadOnly(True)
            self.id_input.setStyleSheet("background-color: #f0f0f0;")
            id_layout.addWidget(self.id_input)
            main_layout.addLayout(id_layout)

        self.inn_input = QLineEdit(customer.get('inn', '') if customer else "")
        inn_validator = QRegularExpressionValidator(QRegularExpression(r"^\d{0,16}$"), self.inn_input)
        self.inn_input.setValidator(inn_validator)
        self.name_input = QLineEdit(customer['name'] if customer else "")
        self.phone_input = QLineEdit(customer['phone'] if customer else "")
        phone_validator = QRegularExpressionValidator(QRegularExpression(r"^\d{0,11}$"), self.phone_input)
        self.phone_input.setValidator(phone_validator)
        self.phone_input.setInputMask("+0(000)000-00-00;_")
        self.email_input = QLineEdit(customer['email'] if customer else "")
        email_validator = QRegularExpressionValidator(QRegularExpression(r"^[^@]+@[^@]+\.[^@]+$"), self.email_input)
        self.email_input.setValidator(email_validator)
        self.address_input = QLineEdit(customer.get('address', '') if customer else "")

        grid_layout = QGridLayout()
        grid_layout.addWidget(QLabel("ИНН:"), 0, 0, alignment=Qt.AlignHCenter)
        grid_layout.addWidget(QLabel("Название:"), 0, 1, alignment=Qt.AlignHCenter)
        grid_layout.addWidget(self.inn_input, 1, 0)
        grid_layout.addWidget(self.name_input, 1, 1)

        grid_layout.addWidget(QLabel("Телефон:"), 2, 0, alignment=Qt.AlignHCenter)
        grid_layout.addWidget(QLabel("Email:"), 2, 1, alignment=Qt.AlignHCenter)
        grid_layout.addWidget(self.phone_input, 3, 0)
        grid_layout.addWidget(self.email_input, 3, 1)

        grid_layout.addWidget(QLabel("Адрес:"), 4, 0, alignment=Qt.AlignHCenter)
        grid_layout.addWidget(self.address_input, 5, 0, 1, 2)
        main_layout.addLayout(grid_layout)

        buttons_layout = QVBoxLayout() 
        buttons_layout.addStretch(1)

        self.save_button = QPushButton("Сохранить")
        self.save_button.setMinimumHeight(50)
        self.save_button.setMinimumWidth(120)
        self.save_button.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        self.save_button.clicked.connect(self.accept)

        self.cancel_button = QPushButton("Отменить")
        self.cancel_button.setMinimumHeight(50)
        self.cancel_button.setMinimumWidth(120)
        self.cancel_button.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        self.cancel_button.clicked.connect(self.reject)

        buttons_layout.addWidget(self.save_button, alignment=Qt.AlignCenter)
        buttons_layout.addWidget(self.cancel_button, alignment=Qt.AlignCenter)
        buttons_layout.addStretch(1)

        main_layout.addLayout(buttons_layout)
        self.setLayout(main_layout)

        for label in self.findChildren(QLabel):
            label.setStyleSheet("font-size: 16px; font-weight: bold;")
        for input_field in self.findChildren(QLineEdit):
            input_field.setMinimumHeight(40)
            input_field.setStyleSheet("font-size: 16px; padding: 5px;")

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def get_data(self):
        return {
            'inn': self.inn_input.text(),
            'name': self.name_input.text(),
            'phone': self.phone_input.text(),
            'email': self.email_input.text(),
            'address': self.address_input.text()
        }
