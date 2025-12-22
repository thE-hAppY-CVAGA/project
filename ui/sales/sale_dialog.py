from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QGridLayout, QComboBox, QLineEdit, QMessageBox, QSpacerItem, QSizePolicy, QWidget, QPushButton
from PyQt6.QtCore import Qt, QRegularExpression
from PyQt6.QtGui import QIntValidator, QRegularExpressionValidator


class SaleDialog(QDialog):
    def __init__(self, db, sale=None, parent=None):
        super().__init__(parent)
        self.db = db
        self.sale = sale
        self.setWindowTitle("Добавить продажу" if sale is None else "Изменить продажу")
        self.setGeometry(200, 200, 500, 400)
        self.center()

        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(15)

        top_layout = QHBoxLayout()
        top_layout.setSpacing(15)

        left_layout = QVBoxLayout()
        left_layout.setSpacing(15)
        left_layout.addWidget(QLabel("Покупатель"), alignment=Qt.AlignCenter)

        self.customer_combo = QComboBox()
        self.customer_combo.setFixedWidth(200)
        self.customer_combo.setMinimumHeight(40)
        self.customers = self.db.get_customers()
        for customer in self.customers:
            self.customer_combo.addItem(customer['name'], customer['id'])
        if sale:
            self.customer_combo.setCurrentIndex(self.customer_combo.findData(sale['customer_id']))
        left_layout.addWidget(self.customer_combo)

        right_layout = QVBoxLayout()
        right_layout.setSpacing(15)
        right_layout.addWidget(QLabel("Сумма"), alignment=Qt.AlignCenter)

        self.total_amount_input = QLineEdit("0.00")
        self.total_amount_input.setFixedWidth(200)
        self.total_amount_input.setMinimumHeight(40)
        self.total_amount_input.setReadOnly(True)
        if sale:
            self.total_amount_input.setText(str(sale['total_amount']))
        right_layout.addWidget(self.total_amount_input)

        top_layout.addLayout(left_layout)
        top_layout.addLayout(right_layout)
        self.main_layout.addLayout(top_layout)

        self.main_layout.addWidget(QLabel("<h2>Продажа</h2>"), alignment=Qt.AlignCenter)

        self.main_grid = QGridLayout()
        self.main_grid.setSpacing(20) 

        self.product_rows = []
        self.current_row = 1 

        self.main_grid.addWidget(QLabel("Товар"), 0, 1, alignment=Qt.AlignLeft)
        self.main_grid.addWidget(QLabel("Количество"), 0, 2, alignment=Qt.AlignLeft)

        self.add_first_product_row()

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)

        self.save_button = QPushButton("Сохранить")
        self.save_button.setMinimumHeight(60)
        self.save_button.setMinimumWidth(150)
        self.save_button.setStyleSheet("font-size: 20px; font-weight: bold; padding: 15px;")
        self.save_button.clicked.connect(self.accept)

        self.cancel_button = QPushButton("Отменить")
        self.cancel_button.setMinimumHeight(60)
        self.cancel_button.setMinimumWidth(150)
        self.cancel_button.setStyleSheet("font-size: 20px; font-weight: bold; padding: 15px;")
        self.cancel_button.clicked.connect(self.reject)

        buttons_layout.addStretch()
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addStretch()

        self.main_layout.addLayout(self.main_grid)
        self.main_layout.addLayout(buttons_layout)
        self.setLayout(self.main_layout)

        for label in self.findChildren(QLabel):
            if "<h2>" not in label.text():  
                label.setStyleSheet("font-size: 16px; font-weight: bold;")
        for input_field in self.findChildren((QComboBox, QLineEdit)):
            input_field.setMinimumHeight(40)
            input_field.setStyleSheet("font-size: 16px; padding: 5px;")

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def add_first_product_row(self):
        row_index = 1

        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(5)
        self.add_item_button = QPushButton("+")
        self.add_item_button.setFixedSize(40, 40)
        self.add_item_button.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.add_item_button.clicked.connect(self.add_product_row)
        self.remove_item_button = QPushButton("-")
        self.remove_item_button.setFixedSize(40, 40)
        self.remove_item_button.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.remove_item_button.clicked.connect(self.remove_product_row)
        buttons_layout.addWidget(self.add_item_button)
        buttons_layout.addWidget(self.remove_item_button)
        self.main_grid.addLayout(buttons_layout, row_index, 0)

        product_combo = QComboBox()
        product_combo.setFixedWidth(200)  
        product_combo.setMinimumHeight(40)  
        product_combo.setStyleSheet("QComboBox { text-align: center; }")  
        self.all_products = self.db.get_products()
        for product in self.all_products:
            product_combo.addItem(f"{product['name']} (цена: {product['price']})", product['id'])
        self.main_grid.addWidget(product_combo, row_index, 1)

        quantity_input = QLineEdit("")
        quantity_input.setFixedWidth(200)  
        quantity_input.setMinimumHeight(40)  
        quantity_input.setAlignment(Qt.AlignCenter)  
        quantity_input.setValidator(QIntValidator(1, 9999, quantity_input))
        self.main_grid.addWidget(quantity_input, row_index, 2)

        self.product_rows.append({
            'combo': product_combo,
            'input': quantity_input,
            'row': row_index
        })

        self.current_row = 3

    def add_product_row(self):

        row_index = self.current_row

        spacer_widget = QWidget()
        spacer_widget.setFixedSize(40, 40)  
        self.main_grid.addWidget(spacer_widget, row_index, 0)

        product_combo = QComboBox()
        product_combo.setFixedWidth(200)  
        product_combo.setMinimumHeight(40)  
        product_combo.setStyleSheet("QComboBox { text-align: center; }")  
        self.all_products = self.db.get_products()
        for product in self.all_products:
            product_combo.addItem(f"{product['name']} (цена: {product['price']})", product['id'])
        self.main_grid.addWidget(product_combo, row_index, 1)

        quantity_input = QLineEdit("")
        quantity_input.setFixedWidth(200)  
        quantity_input.setMinimumHeight(40)  
        quantity_input.setAlignment(Qt.AlignCenter) 
        quantity_input.setValidator(QIntValidator(1, 9999, quantity_input))
        self.main_grid.addWidget(quantity_input, row_index, 2)

        self.product_rows.append({
            'combo': product_combo,
            'input': quantity_input,
            'row': row_index
        })

        self.current_row += 1

    def remove_product_row(self):
  
        if len(self.product_rows) > 1:  

            last_row = self.product_rows.pop()

            self.main_grid.removeWidget(last_row['combo'])
            self.main_grid.removeWidget(last_row['input'])

            last_row['combo'].deleteLater()
            last_row['input'].deleteLater()

            self.current_row -= 1

    def get_data(self):
        customer_id = self.customer_combo.currentData()
        total_amount = 0
        sale_items = []

        for row in self.product_rows:
            product_id = row['combo'].currentData()
            quantity = int(row['input'].text() or "1")
            product_price = next((p['price'] for p in self.all_products if p['id'] == product_id), 0)
            total_amount += quantity * product_price

            sale_items.append({
                'product_id': product_id,
                'quantity': quantity,
                'price': product_price
            })

        return {
            'customer_id': customer_id,
            'total_amount': total_amount,
            'sale_items': sale_items
        }
