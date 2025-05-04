import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget,
    QLineEdit, QListWidget, QHBoxLayout, QMessageBox
)
from utils.helpers import log_event
from utils.account_utils import load_accounts, update_account
from gui.main_window import MainWindow

def main():
    """Entry point for the application."""
    # Log the application start
    log_event("Application started.")

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    result = app.exec_()

    # Log the application end
    log_event("Application ended.")
    sys.exit(result)

if __name__ == "__main__":
    main()