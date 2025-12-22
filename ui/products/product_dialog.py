from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QGridLayout, QMessageBox, QLineEdit, QPushButton, QFormLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator, QDoubleValidator, QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression
from ui.common import BasePage


class ProductDialog(QDialog):
    def __init__(self, db, product=None, parent=None):
        super().__init__(parent)
        self.db = db
        self.product = product
        self.setWindowTitle("Добавить продукт" if product is None else "Изменить продукт")
        self.setGeometry(200, 200, 400, 300)
        self.center()

        self.form_layout = QFormLayout()

        self.name_input = QLineEdit(product['name'] if product else "")
        self.price_input = QLineEdit(str(product['price']) if product else "")
        self.price_input.setValidator(QDoubleValidator(0, 999999999, 2, self.price_input))
        self.quantity_input = QLineEdit(str(product['quantity']) if product else "")
        self.quantity_input.setValidator(QIntValidator(0, 999999, self.quantity_input))
        self.size_input = QLineEdit(product['size'] if product else "")
        size_validator = QRegularExpressionValidator(QRegularExpression(r"^\d*$"), self.size_input)
        self.size_input.setValidator(size_validator)

        grid_layout = QGridLayout()
        grid_layout.addWidget(QLabel("Название:"), 0, 0, alignment=Qt.AlignHCenter)
        grid_layout.addWidget(QLabel("Цена:"), 0, 1, alignment=Qt.AlignHCenter)
        grid_layout.addWidget(self.name_input, 1, 0)
        grid_layout.addWidget(self.price_input, 1, 1)

        grid_layout.addWidget(QLabel("Размер:"), 2, 0, alignment=Qt.AlignHCenter)
        grid_layout.addWidget(QLabel("Количество:"), 2, 1, alignment=Qt.AlignHCenter)
        grid_layout.addWidget(self.size_input, 3, 0)
        grid_layout.addWidget(self.quantity_input, 3, 1)


        self.form_layout.addRow(grid_layout)

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

        main_layout = QVBoxLayout()
        main_layout.addLayout(self.form_layout)
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
            'name': self.name_input.text(),
            'size': self.size_input.text(),
            'price': float(self.price_input.text()),
            'quantity': int(self.quantity_input.text())
        }
