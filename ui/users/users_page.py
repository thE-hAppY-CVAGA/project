from PyQt6.QtWidgets import QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHBoxLayout, QPushButton, QMessageBox, QAbstractItemView, QDialog
from PyQt6.QtCore import Qt
from ui.common import BasePage
from ui.users.user_dialog import UserDialog
import bcrypt


class UsersPage(BasePage):
    def __init__(self, db, parent=None):
        super().__init__(db, parent)
        page_layout = QVBoxLayout()
        self.layout.addLayout(page_layout)

        page_layout.addWidget(QLabel("<h1>Страница пользователей</h1>"), alignment=Qt.AlignmentFlag.AlignCenter)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["№", "Профиль", "Статус", "Последний вход"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        
        self.table.setColumnWidth(0, 150)
        self.table.setColumnWidth(1, 250)
        self.table.setColumnWidth(2, 250)
        self.table.setColumnWidth(3, 300)
        page_layout.addWidget(self.table, 1)

        self.add_button = QPushButton("Добавить")
        self.edit_button = QPushButton("Изменить")
        self.delete_button = QPushButton("Удалить")

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.delete_button)
        buttons_layout.addStretch(1)
        page_layout.addLayout(buttons_layout)

        self.add_button.clicked.connect(self.add_user)
        self.edit_button.clicked.connect(self.edit_user)
        self.delete_button.clicked.connect(self.delete_user)

        self.load_users()

    def load_users(self):
        users = self.db.execute_query("SELECT id, username, role, created_at FROM users ORDER BY username", fetch=True)
        self.table.setRowCount(len(users))
        for i, user in enumerate(users):
            self.table.setItem(i, 0, QTableWidgetItem(str(user['id'])))
            self.table.setItem(i, 1, QTableWidgetItem(user['username']))
            self.table.setItem(i, 2, QTableWidgetItem(user['role']))
            self.table.setItem(i, 3, QTableWidgetItem(user['created_at'].strftime('%d.%m.%Y %H:%M')))

    def add_user(self):
        dialog = UserDialog(self.db)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if data['password'] != data['confirm_password']:
                QMessageBox.warning(self, "Ошибка", "Пароли не совпадают")
                return
            if not data['password']:
                QMessageBox.warning(self, "Ошибка", "Пароль не может быть пустым")
                return

            import re
            if not re.match(r'^[a-zA-Z]+$', data['username']):
                QMessageBox.warning(self, "Ошибка", "Имя пользователя должно содержать только английские буквы")
                return

            if len(data['password']) < 6:
                QMessageBox.warning(self, "Ошибка", "Пароль должен содержать минимум 6 символов")
                return
            if not re.match(r'^[a-zA-Z0-9]+$', data['password']):
                QMessageBox.warning(self, "Ошибка", "Пароль должен содержать только английские буквы и цифры")
                return

            try:
                password_hash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                self.db.execute_query(
                    "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
                    (data['username'], password_hash, data['role'])
                )
                self.load_users()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка добавления пользователя: {e}")

    def edit_user(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Редактирование пользователя", "Выберите пользователя для редактирования")
            return

        row = selected_rows[0].row()
        user_id = int(self.table.item(row, 0).text())
        user_data = self.db.execute_query("SELECT id, username, role FROM users WHERE id = %s", (user_id,), fetch=True)[0]

        dialog = UserDialog(self.db, user=user_data)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()

            import re
            if not re.match(r'^[a-zA-Z]+$', data['username']):
                QMessageBox.warning(self, "Ошибка", "Имя пользователя должно содержать только английские буквы")
                return

            if data['password']:
                if data['password'] != data['confirm_password']:
                    QMessageBox.warning(self, "Ошибка", "Пароли не совпадают")
                    return

                if len(data['password']) < 6:
                    QMessageBox.warning(self, "Ошибка", "Пароль должен содержать минимум 6 символов")
                    return
                if not re.match(r'^[a-zA-Z0-9]+$', data['password']):
                    QMessageBox.warning(self, "Ошибка", "Пароль должен содержать только английские буквы и цифры")
                    return
                password_hash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                self.db.execute_query(
                    "UPDATE users SET username = %s, role = %s, password_hash = %s WHERE id = %s",
                    (data['username'], data['role'], password_hash, user_id)
                )
            else:
                self.db.execute_query(
                    "UPDATE users SET username = %s, role = %s WHERE id = %s",
                    (data['username'], data['role'], user_id)
                )
            self.load_users()

    def delete_user(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Удаление пользователя", "Выберите пользователя для удаления")
            return

        reply = QMessageBox.question(self, 'Удалить пользователя', 'Вы уверены, что хотите удалить выбранного пользователя?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            row = selected_rows[0].row()
            user_id = int(self.table.item(row, 0).text())
            self.db.execute_query("DELETE FROM users WHERE id = %s", (user_id,))
            self.load_users()
