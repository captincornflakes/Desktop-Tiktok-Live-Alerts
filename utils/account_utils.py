import json
import os

ACCOUNTS_FILE = "accounts.json"

def load_accounts():
    """Load accounts from the JSON file."""
    if not os.path.exists(ACCOUNTS_FILE):
        return []
    with open(ACCOUNTS_FILE, 'r') as file:
        return json.load(file)

def save_accounts(accounts):
    """Save accounts to the JSON file."""
    with open(ACCOUNTS_FILE, 'w') as file:
        json.dump(accounts, file, indent=4)

def update_account(tiktok_account, last_online=None, last_checked=None, online=None):
    """Update an account's details or add a new account."""
    accounts = load_accounts()
    for account in accounts:
        if account["tiktok_account"] == tiktok_account:
            if last_online is not None:
                account["last_online"] = last_online
            if last_checked is not None:
                account["last_checked"] = last_checked
            if online is not None:
                account["online"] = online
            save_accounts(accounts)
            return
    # If account doesn't exist, create a new one
    new_account = {
        "tiktok_account": tiktok_account,
        "last_online": last_online or "",
        "last_checked": last_checked or "",
        "online": online or False
    }
    accounts.append(new_account)
    save_accounts(accounts)

def delete_account(tiktok_account):
    """Delete an account from the JSON file."""
    accounts = load_accounts()
    updated_accounts = [account for account in accounts if account["tiktok_account"] != tiktok_account]
    if len(accounts) == len(updated_accounts):
        print(f"Account '{tiktok_account}' not found.")
    else:
        save_accounts(updated_accounts)
        print(f"Account '{tiktok_account}' deleted successfully.")

def create_accounts_file():
    """Create an empty accounts file if it doesn't exist."""
    if not os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, 'w') as file:
            json.dump([], file, indent=4)