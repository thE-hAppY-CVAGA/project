import configparser
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette, QColor
from db import DB


class MainWindow(QMainWindow):
    def __init__(self, username, role):
        super().__init__()
        self.db = DB()
        self.username = username
        self.role = role

        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8')
        app_title = config.get('app', 'title', fallback="Система учета продаж")
        self.setWindowTitle(f"{app_title} - {self.username} ({self.role})")
        self.showMaximized() 

        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        top_panel_layout = QHBoxLayout()

        from datetime import date
        info_label = QLabel(f"Профиль: <b>{self.username}</b>  Роль: <b>{self.role}</b>  Дата: <b>{date.today().strftime('%d.%m.%Y')}</b>")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setStyleSheet("font-size: 36px; font-weight: bold;")

        top_panel_layout.addStretch(1)

        top_panel_layout.addWidget(info_label)

        top_panel_layout.addStretch(1)

        exit_button = QPushButton("Выход")
        exit_button.setObjectName("MainExitButton")
        exit_button.clicked.connect(self.show_login_and_close)
        top_panel_layout.addWidget(exit_button)
        layout.addLayout(top_panel_layout)

        main_content_layout = QHBoxLayout()
        layout.addLayout(main_content_layout)

        self.nav_menu_layout = QVBoxLayout()
        self.nav_menu_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  
        main_content_layout.addLayout(self.nav_menu_layout, 1)

        self.main_content_container = QWidget()
        self.main_content_layout = QVBoxLayout()
        self.main_content_layout.setContentsMargins(0, 0, 0, 0)
        self.main_content_container.setLayout(self.main_content_layout)
        main_content_layout.addWidget(self.main_content_container, 4)

        from ui.products.products_page import ProductsPage
        from ui.sales.sales_page import SalesPage
        from ui.customers.customers_page import CustomersPage
        from ui.reports.reports_page import ReportsPage
        from ui.users.users_page import UsersPage

        self.products_page = ProductsPage(self.db)
        self.sales_page = SalesPage(self.db)
        self.customers_page = CustomersPage(self.db)
        self.reports_page = ReportsPage(self.db)
        self.users_page = UsersPage(self.db)

        self.current_page = self.products_page
        self.main_content_layout.addWidget(self.current_page)

        self.products_button = QPushButton("Товар")
        self.sales_button = QPushButton("Продажи")
        self.customers_button = QPushButton("Покупатели")
        self.reports_button = QPushButton("Отчет")
        self.users_button = QPushButton("Пользователи")

        self.nav_menu_layout.addWidget(self.products_button)
        self.nav_menu_layout.addWidget(self.sales_button)
        self.nav_menu_layout.addWidget(self.customers_button)
        self.nav_menu_layout.addWidget(self.reports_button)
        if self.role == 'admin':
            self.nav_menu_layout.addWidget(self.users_button)

        self.products_button.clicked.connect(lambda: self.switch_page(self.products_page))
        self.sales_button.clicked.connect(lambda: self.switch_page(self.sales_page))
        self.customers_button.clicked.connect(lambda: self.switch_page(self.customers_page))
        self.reports_button.clicked.connect(lambda: self.switch_page(self.reports_page))
        if self.role == 'admin':
            self.users_button.clicked.connect(lambda: self.switch_page(self.users_page))

        self.apply_styles()

    def switch_page(self, new_page):

        if self.current_page is not None:
            self.main_content_layout.removeWidget(self.current_page)
            self.current_page.setParent(None)

        self.current_page = new_page
        self.main_content_layout.addWidget(self.current_page)

    def show_login_and_close(self):

        from ui.auth.login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()

        self.close()

    def apply_styles(self):
 
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#FFFFFF"))  
        palette.setColor(QPalette.ColorRole.WindowText, QColor("#000000")) 
        palette.setColor(QPalette.ColorRole.Base, QColor("#FFFFFF"))    
        palette.setColor(QPalette.ColorRole.Text, QColor("#000000"))     
        palette.setColor(QPalette.ColorRole.Button, QColor("#FFFFFF")) 
        palette.setColor(QPalette.ColorRole.ButtonText, QColor("#000000")) 
        self.setPalette(palette)

        font = QFont("Segoe UI", 12)
        QApplication.setFont(font)

        self.setStyleSheet("""
            QLabel {
                color: #000000;
                font-size: 36px; 
                font-weight: bold;
            }
            QLineEdit {
                border: 2px solid #CCCCCC;
                border-radius: 8px;
                padding: 16px;
                font-size: 32px; 
                background-color: #FFFFFF;
            }
            QPushButton {
                background-color: #FFFFFF;
                color: #000000;
                border: 1px solid #CCCCCC; 
                border-radius: 8px; 
                padding: 20px 40px; 
                font-size: 24px; 
                font-weight: bold;
                border-radius: 8px; 
            }
            QPushButton:hover {
                background-color: #F0F0F0;
            }
            QPushButton#MainExitButton {
                background-color: #FFFFFF; 
                color: #000000; 
                border: 1px solid #CCCCCC; 
                border-radius: 8px;
                padding: 15px 30px; 
                font-size: 20px; 
                font-weight: bold;
            }
            QPushButton#MainExitButton:hover {
                background-color: #F0F0F0; 
            }
            QLineEdit {
                border: 1px solid #CCCCCC; 
                border-radius: 8px;
                padding: 8px; 
                font-size: 14px; 
                background-color: #FFFFFF;
                color: #000000; 
            }
            QLabel {
                color: #000000; 
                font-size: 16px; 
            }
            QCheckBox {
                color: #000000; 
                font-size: 16px; 
            }
            QTabWidget::pane {
                border: 1px solid #CCCCCC;
                background-color: #FFFFFF;
            }
            QTabBar::tab {
                background: #E0E0E0;
                border: 1px solid #CCCCCC;
                border-bottom-color: #CCCCCC; 
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                min-width: 8ex;
                padding: 8px;
            }
            QTabBar::tab:selected, QTabBar::tab:hover {
                background: #F0F0F0;
            }
            QTabBar::tab:selected {
                border-color: #999999;
                border-bottom-color: #F0F0F0; 
            }
            QBoxLayout#nav_menu_layout QPushButton {
                background-color: #FFFFFF; 
                color: #000000; 
                border: 1px solid #CCCCCC;
                border-radius: 8px;
                padding: 12px; 
                font-size: 16px; 
                text-align: center; 
                margin-bottom: 8px; 
            }
            QBoxLayout#nav_menu_layout QPushButton:hover {
                background-color: #F0F0F0; 
            }
            QBoxLayout#nav_menu_layout QPushButton:checked { 
                background-color: #F0F0F0; 
                border-color: #CCCCCC;
            }
            QTableWidget {
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                gridline-color: #E0E0E0;
                background-color: #FFFFFF;
                qproperty-sizePolicy: expanding expanding;
            }
            QHeaderView::section {
                background-color: #FFFFFF; 
                color: #000000; 
                padding: 12px 40px; 
                border: 1px solid #CCCCCC;
                font-weight: bold;
                font-size: 24px; 
                text-align: center;
                qproperty-alignment: AlignCenter; 
            }
            QTableWidget::item {
                padding: 8px; 
                font-size: 14px; 
                color: #000000; 
                text-align: center; 
                qproperty-textAlignment: AlignCenter; 
            }
            QTableWidget::item:selected {
                background-color: #F0F0F0; 
                color: #000000; 
            }
            QDialogButtonBox QPushButton {
                background-color: #FFFFFF; 
                color: #000000; 
                border: 1px solid #CCCCCC; 
                border-radius: 8px;
                padding: 8px 16px; 
                font-size: 14px; 
            }
            QDialogButtonBox QPushButton:hover {
                background-color: #F0F0F0;
            }
            QComboBox {
                border: 1px solid #CCCCCC;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px; 
                background-color: #FFFFFF;
                color: #000000; 
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #999999;
                border-left-style: solid;
                border-top-right-radius: 8px;
                border-bottom-right-radius: 8px;
            }
            QDateTimeEdit {
                border: 1px solid #CCCCCC; 
                border-radius: 8px;
                padding: 8px; 
                font-size: 14px; 
                background-color: #FFFFFF;
                color: #000000; 
            }
            QDateTimeEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #999999;
                border-left-style: solid;
                border-top-right-radius: 8px;
                border-bottom-right-radius: 8px;
            }
        """)
