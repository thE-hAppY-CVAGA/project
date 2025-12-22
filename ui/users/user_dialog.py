from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QGridLayout, QLineEdit, QComboBox, QMessageBox, QPushButton, QFormLayout
from PyQt6.QtCore import Qt, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator


class UserDialog(QDialog):
    def __init__(self, db, user=None, parent=None):
        super().__init__(parent)
        self.db = db
        self.user = user
        self.setWindowTitle("Добавить пользователя" if user is None else "Изменить пользователя")
        self.center()
        self.setMinimumSize(400, 450)

        self.form_layout = QFormLayout()

        self.id_input = QLineEdit("")
        self.id_input.setReadOnly(True)
        self.id_input.setStyleSheet("background-color: #f0f0f0;")  
        if user:
            self.id_input.setText(str(user['id']))
            self.form_layout.addRow("№:", self.id_input)

        self.username_input = QLineEdit(user['username'] if user else "")
        username_validator = QRegularExpressionValidator(QRegularExpression(r"^[a-zA-Z]+$"), self.username_input)
        self.username_input.setValidator(username_validator)

        self.role_combo = QComboBox()
        self.role_combo.addItem("user")
        self.role_combo.addItem("admin")
        self.role_combo.setStyleSheet("""
            QComboBox {
                font-size: 16px; 
                padding: 5px; 
                background-color: #000000; /* Black background for the main part */
                color: #ffffff; /* White text for the main part */
                border: 1px solid #555555; 
            }

            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #555555;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
                background-color: #000000; /* Black background for the dropdown arrow */
                color: #ffffff; /* White arrow */
            }

            QComboBox::down-arrow {
                image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeTAAAAV0lEQVQ4jWNgGAWjYBRgBIJ/wQcQjVnIAoT/g/83A7EQG5jADoP/MwC/gNlMgLpA/g/YGAoGxkIgsT/BfwYgABXhT4i2AT+EwB+J7m0gFoJGAWjYBRgAADLswb/C00+WwAAAABJRU5ErkJggg==); /* Пример белой стрелки */
            }

            QComboBox QAbstractItemView {
                border: 1px solid #555555;
                background-color: #000000; /* Black background for the dropdown list itself */
                selection-background-color: #333333; /* Darker gray on hover/selection */
                color: #ffffff; /* White text for items in the dropdown */
            }

            QComboBox QAbstractItemView::item {
                height: 30px; /* Увеличиваем высоту элементов для лучшей читаемости */
            }

            QComboBox QAbstractItemView::item:selected {
                background-color: #333333; /* Darker gray for selected item */
                color: #ffffff;
            }
        """)
        if user:
            self.role_combo.setCurrentText(user['role'])

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        password_validator = QRegularExpressionValidator(QRegularExpression(r"^[a-zA-Z0-9]+$"), self.password_input)
        self.password_input.setValidator(password_validator)
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        confirm_validator = QRegularExpressionValidator(QRegularExpression(r"^[a-zA-Z0-9]*$"), self.confirm_password_input)
        self.confirm_password_input.setValidator(confirm_validator)

        grid_layout = QGridLayout()
        grid_layout.addWidget(QLabel("Профиль:"), 0, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        grid_layout.addWidget(QLabel("Статус:"), 0, 1, alignment=Qt.AlignmentFlag.AlignHCenter)
        grid_layout.addWidget(self.username_input, 1, 0)
        grid_layout.addWidget(self.role_combo, 1, 1)

        # Spacer for 30 pixels below role_combo
        spacer_label_password = QLabel()
        spacer_label_password.setFixedHeight(70)
        grid_layout.addWidget(spacer_label_password, 2, 0, 1, 2) # Row 2, spanning 2 columns

        grid_layout.addWidget(QLabel("Пароль:"), 3, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        grid_layout.addWidget(QLabel("Повтор. пароля:"), 3, 1, alignment=Qt.AlignmentFlag.AlignHCenter)
        grid_layout.addWidget(self.password_input, 4, 0)
        grid_layout.addWidget(self.confirm_password_input, 4, 1)

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

        buttons_layout.addWidget(self.save_button, alignment=Qt.AlignmentFlag.AlignCenter)
        buttons_layout.addWidget(self.cancel_button, alignment=Qt.AlignmentFlag.AlignCenter)
        buttons_layout.addStretch(1)

        main_layout = QVBoxLayout()
        main_layout.addLayout(self.form_layout)
        main_layout.addLayout(buttons_layout)
        self.setLayout(main_layout)
        self.adjustSize()

        for label in self.findChildren(QLabel):
            label.setStyleSheet("font-size: 16px; font-weight: bold;")
        for input_field in self.findChildren((QLineEdit, QComboBox)):
            input_field.setMinimumHeight(40)
            input_field.setStyleSheet("font-size: 16px; padding: 5px;")

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def get_data(self):
        return {
            'username': self.username_input.text(),
            'role': self.role_combo.currentText(),
            'password': self.password_input.text(),
            'confirm_password': self.confirm_password_input.text()
        }
