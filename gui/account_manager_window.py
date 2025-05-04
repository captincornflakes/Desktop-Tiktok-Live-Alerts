from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QLineEdit, QPushButton, QListWidget, QWidget, QMessageBox, QHBoxLayout, QListWidgetItem, QLabel
)
from PyQt5.QtCore import Qt
from utils.account_utils import load_accounts, update_account, delete_account

class AccountManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manage Accounts")
        self.setGeometry(150, 150, 600, 800)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Input box and button to add a new account
        self.account_input = QLineEdit(self)
        self.account_input.setPlaceholderText("Enter TikTok account")
        layout.addWidget(self.account_input)

        add_button = QPushButton("Add Account", self)
        add_button.clicked.connect(self.add_account)
        layout.addWidget(add_button)

        # List to display accounts
        self.account_list = QListWidget(self)
        layout.addWidget(self.account_list)

        # Load accounts into the list
        self.load_accounts()

        # Set the central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_accounts(self):
        """Load accounts from the JSON file and display them with delete buttons."""
        self.account_list.clear()
        accounts = load_accounts()
        for account in accounts:
            # Create a horizontal layout for each account
            item_widget = QWidget()
            item_layout = QHBoxLayout()
            item_layout.setContentsMargins(0, 0, 0, 0)

            # Add account name and status
            account_label = QLabel(f"{account['tiktok_account']} - Online: {account['online']}")
            item_layout.addWidget(account_label)

            # Add delete button
            delete_button = QPushButton("X", self)
            delete_button.setStyleSheet("color: red; font-weight: bold;")
            delete_button.clicked.connect(lambda _, acc=account['tiktok_account']: self.delete_account(acc))
            item_layout.addWidget(delete_button)

            # Set the layout to the widget and add it to the list
            item_widget.setLayout(item_layout)
            list_item = QListWidgetItem(self.account_list)
            list_item.setSizeHint(item_widget.sizeHint())
            self.account_list.addItem(list_item)
            self.account_list.setItemWidget(list_item, item_widget)

    def add_account(self):
        """Add a new account to the JSON file."""
        account_name = self.account_input.text().strip()
        if not account_name:
            QMessageBox.warning(self, "Input Error", "Please enter a TikTok account name.")
            return

        update_account(tiktok_account=account_name, online=False)
        self.account_input.clear()
        self.load_accounts()
        QMessageBox.information(self, "Success", f"Account '{account_name}' added successfully.")

    def delete_account(self, tiktok_account):
        """Delete an account from the JSON file."""
        confirm = QMessageBox.question(
            self,
            "Delete Account",
            f"Are you sure you want to delete the account '{tiktok_account}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            delete_account(tiktok_account)
            self.load_accounts()
            QMessageBox.information(self, "Success", f"Account '{tiktok_account}' deleted successfully.")