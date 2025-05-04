# TikTok Live Checker

## Overview
This project is a Python-based GUI application designed to provide a user-friendly interface for interacting with TikTok live accounts. It includes a structured layout for assets, logging, and utility functions.

## Project Structure
```
TikTok Live Checker
├── gui
│   ├── account_manager_window.py  # GUI for managing TikTok accounts
│   └── main_window.py             # Main GUI window for the application
├── logs
│   └── app.log                    # Log file for application events and errors
├── utils
│   ├── helpers.py                 # Utility functions for common tasks
│   ├── account_utils.py           # Functions for managing TikTok accounts
│   └── sound_handler.py           # Functions for playing sound notifications
├── accounts.json                  # JSON file for storing TikTok account data
├── requirements.txt               # Lists project dependencies
├── README.md                      # Documentation for the project
├── main.py                        # Entry point for the application
└── __init__.py                    # Marks the directory as a Python package
```

## Setup Instructions
1. Clone the repository:
   ```
   git clone <repository-url>
   cd TikTok-Live-Checker
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python main.py
   ```

## Usage
- The application provides a graphical interface for users to manage TikTok accounts and check their live status.
- Static assets such as sounds should be placed in the `sounds` folder.
- Application logs will be recorded in the `logs/app.log`.

## Features
- **Account Management**: Add, delete, and view TikTok accounts.
- **Live Status Checker**: Automatically checks if TikTok accounts are live at regular intervals.
- **Notifications**: Plays a sound and shows a desktop notification when an account goes live.
- **Logging**: Logs all events and errors to `logs/app.log`.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.