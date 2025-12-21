from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHBoxLayout, QPushButton, QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QComboBox, QSpinBox, QDateTimeEdit, QAbstractSpinBox, QMessageBox, QHeaderView, QGridLayout, QAbstractItemView
from PyQt6.QtCore import Qt, QDateTime, QRegularExpression
from PyQt6.QtGui import QIntValidator, QDoubleValidator, QRegularExpressionValidator
from db import DB

class BasePage(QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setup_ui()

    def setup_ui(self):
        pass
