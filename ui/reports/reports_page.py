from PyQt6.QtWidgets import QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHBoxLayout, QPushButton, QDateTimeEdit, QAbstractItemView, QAbstractSpinBox
from PyQt6.QtCore import Qt, QDateTime
from ui.common import BasePage


class ReportsPage(BasePage):
    def __init__(self, db, parent=None):
        super().__init__(db, parent)
        page_layout = QVBoxLayout()
        page_layout.setContentsMargins(10, 10, 30, 10)  
        self.layout.addLayout(page_layout)

        page_layout.addWidget(QLabel("<h1>Страница отчетов</h1>"), alignment=Qt.AlignmentFlag.AlignCenter)

        date_selection_layout = QHBoxLayout()
        date_selection_layout.addStretch(1)  

        period_label = QLabel("Период")
        period_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        period_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        date_selection_layout.addWidget(period_label)

        date_from_label = QLabel("с")
        date_from_label.setStyleSheet("font-size: 20px;")
        date_selection_layout.addWidget(date_from_label)

        self.date_from = QDateTimeEdit(QDateTime.currentDateTime())
        self.date_from.setCalendarPopup(True)
        self.date_from.setDisplayFormat("dd.MM.yyyy")
        self.date_from.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.date_from.setStyleSheet("font-size: 18px; padding: 10px;")
        date_selection_layout.addWidget(self.date_from)

        date_to_label = QLabel("по")
        date_to_label.setStyleSheet("font-size: 20px;")
        date_selection_layout.addWidget(date_to_label)

        self.date_to = QDateTimeEdit(QDateTime.currentDateTime())
        self.date_to.setCalendarPopup(True)
        self.date_to.setDisplayFormat("dd.MM.yyyy")
        self.date_to.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.date_to.setStyleSheet("font-size: 18px; padding: 10px;")
        date_selection_layout.addWidget(self.date_to)

        self.generate_report_button = QPushButton("Сформировать")
        self.generate_report_button.setStyleSheet("font-size: 24px; font-weight: bold; padding: 20px 40px;")
        self.generate_report_button.clicked.connect(self.generate_report)
        date_selection_layout.addWidget(self.generate_report_button)

        date_selection_layout.addStretch(1)
        page_layout.addLayout(date_selection_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Товар", "Продано", "Средняя цена", "Выручка"])
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)

        self.table.setColumnWidth(0, 300)
        self.table.setColumnWidth(1, 250)
        self.table.setColumnWidth(2, 250)
        self.table.setColumnWidth(3, 300)

        self.table.verticalHeader().setDefaultSectionSize(60)
        page_layout.addWidget(self.table, 1)  

    def generate_report(self):
        start_date = self.date_from.dateTime().toString("yyyy-MM-dd")
        end_date = self.date_to.dateTime().toString("yyyy-MM-dd")

        report_data = self.db.execute_query(
            """
            SELECT
                p.name as product_name,
                SUM(si.quantity) as total_quantity_sold,
                AVG(si.price) as average_price,
                SUM(si.quantity * si.price) as total_revenue
            FROM sales s
            JOIN sale_items si ON s.id = si.sale_id
            JOIN products p ON si.product_id = p.id
            WHERE s.sale_date::date BETWEEN %s AND %s
            GROUP BY p.name
            ORDER BY p.name
            """,
            (start_date, end_date),
            fetch=True
        )

        self.table.setRowCount(len(report_data))
        for i, row in enumerate(report_data):
            self.table.setItem(i, 0, QTableWidgetItem(row['product_name']))
            self.table.setItem(i, 1, QTableWidgetItem(str(row['total_quantity_sold'])))
            self.table.setItem(i, 2, QTableWidgetItem(f"{row['average_price']:.2f}"))
            self.table.setItem(i, 3, QTableWidgetItem(f"{row['total_revenue']:.2f}"))
