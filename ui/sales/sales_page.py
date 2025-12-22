from PyQt6.QtWidgets import QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHBoxLayout, QPushButton, QMessageBox, QAbstractItemView, QDialog
from PyQt6.QtCore import Qt
from ui.common import BasePage
from ui.sales.sale_dialog import SaleDialog


class SalesPage(BasePage):
    def __init__(self, db, parent=None):
        super().__init__(db, parent)
        page_layout = QVBoxLayout()
        page_layout.setContentsMargins(10, 10, 30, 10)
        self.layout.addLayout(page_layout)

        page_layout.addWidget(QLabel("<h1>Страница продаж</h1>"), alignment=Qt.AlignmentFlag.AlignCenter)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["№", "Покупатели", "Продажа", "Сумма", "Дата"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setColumnWidth(0, 150)
        self.table.setColumnWidth(1, 250)
        self.table.setColumnWidth(2, 300)
        self.table.setColumnWidth(3, 250)
        self.table.setColumnWidth(4, 200)
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

        self.add_button.clicked.connect(self.add_sale)
        self.edit_button.clicked.connect(self.edit_sale)
        self.delete_button.clicked.connect(self.delete_sale)

        self.load_sales()

    def load_sales(self):
        sales = self.db.get_sales()
        self.table.setRowCount(len(sales))
        for i, sale in enumerate(sales):
            self.table.setItem(i, 0, QTableWidgetItem(str(sale['id'])))
            self.table.setItem(i, 1, QTableWidgetItem(sale['customer_name'] if sale['customer_name'] else "Неизвестно"))
            self.table.setItem(i, 2, QTableWidgetItem(str(sale['items_count'])))
            self.table.setItem(i, 3, QTableWidgetItem(str(sale['total_amount'])))
            self.table.setItem(i, 4, QTableWidgetItem(sale['sale_date'].strftime('%d.%m.%Y %H:%M')))

    def add_sale(self):
        dialog = SaleDialog(self.db)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            sale_id = self.db.execute_query(
                "INSERT INTO sales (customer_id, total_amount, user_id) VALUES (%s, %s, %s) RETURNING id",
                (data['customer_id'], data['total_amount'], 1), 
                fetch=True
            )[0]['id']

            for item in data['sale_items']:
                self.db.execute_query(
                    "INSERT INTO sale_items (sale_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
                    (sale_id, item['product_id'], item['quantity'], item['price'])
                )
            self.load_sales()

    def edit_sale(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Редактирование продажи", "Выберите продажу для редактирования")
            return

        row = selected_rows[0].row()
        sale_id = int(self.table.item(row, 0).text())
        sale_data = self.db.execute_query("SELECT * FROM sales WHERE id = %s", (sale_id,), fetch=True)[0]

        dialog = SaleDialog(self.db, sale=sale_data) 
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            self.db.execute_query(
                "UPDATE sales SET customer_id = %s, total_amount = %s WHERE id = %s",
                (data['customer_id'], data['total_amount'], sale_id)
            )

            self.db.execute_query("DELETE FROM sale_items WHERE sale_id = %s", (sale_id,))
            for item in data['sale_items']:
                self.db.execute_query(
                    "INSERT INTO sale_items (sale_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
                    (sale_id, item['product_id'], item['quantity'], item['price'])
                )
            self.load_sales()

    def delete_sale(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Удаление продажи", "Выберите продажу для удаления")
            return

        reply = QMessageBox.question(self, 'Удалить продажу', 'Вы уверены, что хотите удалить выбранную продажу?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            row = selected_rows[0].row()
            sale_id = int(self.table.item(row, 0).text())
            self.db.execute_query("DELETE FROM sale_items WHERE sale_id = %s", (sale_id,))
            self.db.execute_query("DELETE FROM sales WHERE id = %s", (sale_id,))
            self.load_sales()

    def refresh_data(self):
        """Обновляет данные в таблице"""
        self.load_sales()
