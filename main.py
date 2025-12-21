import sys
from PyQt6.QtWidgets import QApplication
from db import DB
import traceback

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        from ui.auth.login_window import LoginWindow
        login_win = LoginWindow()
        login_win.show()
        sys.exit(app.exec())
    except KeyboardInterrupt:
        print("\nПрограмма была прервана пользователем")
        sys.exit(0)
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        traceback.print_exc()
        sys.exit(1)