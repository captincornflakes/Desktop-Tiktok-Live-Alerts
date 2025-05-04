from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QComboBox, QMessageBox, QListWidget
)
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
import asyncio
from gui.account_manager_window import AccountManagerWindow
from utils.live_checker import LiveChecker
from utils.account_utils import load_accounts
import time

class LiveCheckerThread(QThread):
    log_signal = pyqtSignal(str)
    new_live_signal = pyqtSignal(str)  # Signal to notify when a new live account is found

    def __init__(self, interval):
        super().__init__()
        self.interval = interval
        self.live_checker = LiveChecker()
        self.running = False

    def run(self):
        """Run the live checker in an asyncio event loop."""
        self.running = True
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.run_checker())
        except asyncio.CancelledError:
            pass
        finally:
            loop.close()

    async def run_checker(self):
        """Run the live checker in a loop."""
        while self.running:
            try:
                await self.live_checker.check_accounts(self.interval, self.new_live_signal)
                self.log_signal.emit("Live checker completed a cycle.")
            except Exception as e:
                self.log_signal.emit(f"Error in live checker: {str(e)}")
            await asyncio.sleep(self.interval * 60)

    def stop(self):
        """Stop the live checker."""
        self.running = False
        self.live_checker.stop()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TikTok Live Checker")
        self.setGeometry(100, 100, 800, 800)
        self.live_checker_thread = None
        self.countdown_timer = None
        self.remaining_time = 0
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Top horizontal layout for buttons and dropdown
        top_layout = QHBoxLayout()

        # Manage Accounts button
        manage_accounts_button = QPushButton("Manage Accounts", self)
        manage_accounts_button.clicked.connect(self.open_account_manager)
        top_layout.addWidget(manage_accounts_button)

        # Start/Stop Live Checker button
        self.live_checker_button = QPushButton("Start Live Checker", self)
        self.live_checker_button.clicked.connect(self.toggle_live_checker)
        top_layout.addWidget(self.live_checker_button)

        # Interval label
        interval_label = QLabel("Interval (minutes):", self)
        top_layout.addWidget(interval_label)

        # Dropdown for interval selection
        self.interval_dropdown = QComboBox(self)
        self.interval_dropdown.addItems(["1", "5", "10", "15", "30", "60"])
        top_layout.addWidget(self.interval_dropdown)

        # Add the top layout to the main layout
        main_layout.addLayout(top_layout)

        # Countdown label
        self.countdown_label = QLabel("Next check in: --:--", self)
        main_layout.addWidget(self.countdown_label)

        # Live accounts list
        self.live_accounts_label = QLabel("Live Accounts:", self)
        main_layout.addWidget(self.live_accounts_label)

        self.live_accounts_list = QListWidget(self)
        main_layout.addWidget(self.live_accounts_list)

        # Set the central widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def open_account_manager(self):
        """Open the Account Manager window."""
        self.account_manager_window = AccountManagerWindow()
        self.account_manager_window.show()

    def toggle_live_checker(self):
        """Start or stop the live checker."""
        if self.live_checker_thread and self.live_checker_thread.isRunning():
            # Stop the live checker
            self.live_checker_thread.stop()
            self.live_checker_thread = None
            self.live_checker_button.setText("Start Live Checker")
            self.stop_countdown()
            QMessageBox.information(self, "Live Checker", "Live checker stopped.")
        else:
            # Start the live checker
            interval = int(self.interval_dropdown.currentText())
            self.live_checker_thread = LiveCheckerThread(interval)
            self.live_checker_thread.log_signal.connect(self.log_message)
            self.live_checker_thread.new_live_signal.connect(self.update_live_accounts)  # Connect the signal
            self.live_checker_thread.start()
            self.start_countdown(interval)
            self.live_checker_button.setText("Stop Live Checker")
            QMessageBox.information(self, "Live Checker", f"Live checker started with {interval}-minute interval.")

    def start_countdown(self, interval):
        """Start the countdown timer."""
        self.remaining_time = interval * 60  # Convert minutes to seconds
        self.update_countdown_label()
        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.countdown_timer.start(1000)  # Update every second

    def stop_countdown(self):
        """Stop the countdown timer."""
        if self.countdown_timer:
            self.countdown_timer.stop()
            self.countdown_label.setText("Next check in: --:--")

    def update_countdown(self):
        """Update the countdown timer."""
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.update_countdown_label()
        else:
            self.update_live_accounts()
            interval = int(self.interval_dropdown.currentText())
            self.start_countdown(interval)  # Restart the countdown

    def update_countdown_label(self):
        """Update the countdown label with the remaining time."""
        minutes, seconds = divmod(self.remaining_time, 60)
        self.countdown_label.setText(f"Next check in: {minutes:02}:{seconds:02}")

    def update_live_accounts(self):
        """Update the list of live accounts."""
        self.live_accounts_list.clear()
        accounts = load_accounts()
        live_accounts = [account["tiktok_account"] for account in accounts if account["online"]]

        if live_accounts:
            self.live_accounts_list.addItems(live_accounts)
        else:
            self.live_accounts_list.addItem("No current lives")

    def log_message(self, message):
        """Log messages from the live checker thread."""
        print(message)  # Replace with a GUI log display if needed