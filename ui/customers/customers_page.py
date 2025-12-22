from PyQt6.QtWidgets import QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHBoxLayout, QPushButton, QMessageBox, QAbstractItemView, QDialog
from PyQt6.QtCore import Qt
from ui.common import BasePage
from ui.customers.customer_dialog import CustomerDialog


class CustomersPage(BasePage):
    def __init__(self, db, parent=None):
        super().__init__(db, parent)
        page_layout = QVBoxLayout()
        page_layout.setContentsMargins(10, 10, 30, 10)
        self.layout.addLayout(page_layout)

        page_layout.addWidget(QLabel("<h1>Страница клиентов</h1>"), alignment=Qt.AlignmentFlag.AlignCenter)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["№", "ИНН", "Название", "Телефон", "Кол-во покупок", "Адрес"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setColumnWidth(0, 120)
        self.table.setColumnWidth(1, 180)
        self.table.setColumnWidth(2, 200)
        self.table.setColumnWidth(3, 200)
        self.table.setColumnWidth(4, 270)
        self.table.setColumnWidth(5, 175)
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

        self.add_button.clicked.connect(self.add_customer)
        self.edit_button.clicked.connect(self.edit_customer)
        self.delete_button.clicked.connect(self.delete_customer)

        self.load_customers()

    def load_customers(self):
        customers = self.db.get_customers()
        self.table.setRowCount(len(customers))
        for i, customer in enumerate(customers):

            purchases_count = self.db.execute_query(
                "SELECT COUNT(*) as count FROM sales WHERE customer_id = %s",
                (customer['id'],),
                fetch=True
            )[0]['count']

            self.table.setItem(i, 0, QTableWidgetItem(str(customer['id'])))
            self.table.setItem(i, 1, QTableWidgetItem(customer.get('inn', '')))  
            self.table.setItem(i, 2, QTableWidgetItem(customer['name']))
            self.table.setItem(i, 3, QTableWidgetItem(customer['phone'] or ""))
            self.table.setItem(i, 4, QTableWidgetItem(str(purchases_count)))
            self.table.setItem(i, 5, QTableWidgetItem(customer['address'] or ""))

    def add_customer(self):
        dialog = CustomerDialog(self.db)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()

            if not data['name'].strip():
                QMessageBox.warning(self, "Ошибка", "Название клиента не может быть пустым")
                return
            if data['email'] and '@' not in data['email']:
                QMessageBox.warning(self, "Ошибка", "Email должен содержать символ @")
                return

            self.db.execute_query(
                "INSERT INTO customers (name, phone, email, address, inn) VALUES (%s, %s, %s, %s, %s)",
                (data['name'], data['phone'], data['email'], data['address'], data['inn'])
            )
            self.load_customers()

    def edit_customer(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Редактирование клиента", "Выберите клиента для редактирования")
            return

        row = selected_rows[0].row()
        customer_id = int(self.table.item(row, 0).text())
        customer_data = self.db.execute_query(
            "SELECT * FROM customers WHERE id = %s", (customer_id,), fetch=True
        )[0]

        dialog = CustomerDialog(self.db, customer=customer_data)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()

            if not data['name'].strip():
                QMessageBox.warning(self, "Ошибка", "Название клиента не может быть пустым")
                return
            if data['email'] and '@' not in data['email']:
                QMessageBox.warning(self, "Ошибка", "Email должен содержать символ @")
                return

            self.db.execute_query(
                "UPDATE customers SET name = %s, phone = %s, email = %s, address = %s, inn = %s WHERE id = %s",
                (data['name'], data['phone'], data['email'], data['address'], data['inn'], customer_id)
            )
            self.load_customers()

    def delete_customer(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Удаление клиента", "Выберите клиента для удаления")
            return

        reply = QMessageBox.question(self, 'Удалить клиента', 'Вы уверены, что хотите удалить выбранного клиента?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            row = selected_rows[0].row()
            customer_id = int(self.table.item(row, 0).text())
            self.db.execute_query("DELETE FROM customers WHERE id = %s", (customer_id,))
            self.load_customers()
