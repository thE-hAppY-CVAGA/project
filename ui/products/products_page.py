from PyQt6.QtWidgets import QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHBoxLayout, QPushButton, QMessageBox, QAbstractItemView, QDialog
from PyQt6.QtCore import Qt
from ui.common import BasePage
from ui.products.product_dialog import ProductDialog


class ProductsPage(BasePage):
    def __init__(self, db, parent=None):
        super().__init__(db, parent)
        page_layout = QVBoxLayout()
        page_layout.setContentsMargins(10, 10, 30, 10)
        self.layout.addLayout(page_layout)

        page_layout.addWidget(QLabel("<h1>Страница продуктов</h1>"), alignment=Qt.AlignmentFlag.AlignCenter)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["№", "Наименование", "Размер", "Цена", "Кол-во"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)

        self.table.setColumnWidth(0, 150)   
        self.table.setColumnWidth(1, 280)  
        self.table.setColumnWidth(2, 230)  
        self.table.setColumnWidth(3, 240)  
        self.table.setColumnWidth(4, 220)   
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

        self.add_button.clicked.connect(self.add_product)
        self.edit_button.clicked.connect(self.edit_product)
        self.delete_button.clicked.connect(self.delete_product)

        self.load_products()

    def load_products(self):
        products = self.db.get_products()
        self.table.setRowCount(len(products))
        for i, product in enumerate(products):
            self.table.setItem(i, 0, QTableWidgetItem(str(product['id'])))
            self.table.setItem(i, 1, QTableWidgetItem(product['name']))
            self.table.setItem(i, 2, QTableWidgetItem(product['size']))
            self.table.setItem(i, 3, QTableWidgetItem(str(product['price'])))
            self.table.setItem(i, 4, QTableWidgetItem(str(product['quantity'])))

    def add_product(self):
        dialog = ProductDialog(self.db)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            self.db.execute_query(
                "INSERT INTO products (name, size, price, quantity) VALUES (%s, %s, %s, %s)",
                (data['name'], data['size'], data['price'], data['quantity'])
            )
            self.load_products()

    def edit_product(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Редактирование продукта", "Выберите продукт для редактирования")
            return

        row = selected_rows[0].row()
        product_id = int(self.table.item(row, 0).text())
        product_data = self.db.execute_query(
            "SELECT * FROM products WHERE id = %s", (product_id,), fetch=True
        )[0]

        dialog = ProductDialog(self.db, product=product_data)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            self.db.execute_query(
                "UPDATE products SET name = %s, size = %s, price = %s, quantity = %s WHERE id = %s",
                (data['name'], data['size'], data['price'], data['quantity'], product_id)
            )
            self.load_products()

    def delete_product(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Удаление продукта", "Выберите продукт для удаления")
            return

        reply = QMessageBox.question(self, 'Удалить продукт', 'Вы уверены, что хотите удалить выбранный продукт?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            row = selected_rows[0].row()
            product_id = int(self.table.item(row, 0).text())
            self.db.execute_query("DELETE FROM products WHERE id = %s", (product_id,))
            self.load_products()
