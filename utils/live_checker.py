import asyncio
from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent
from utils.helpers import log_event
from utils.account_utils import load_accounts, update_account
from datetime import datetime
from utils.sound_handler import play_alert_sound
from plyer import notification

class LiveChecker:
    def __init__(self):
        self.clients = {}
        self.running = False

    async def check_accounts(self, interval, new_live_signal):
        """Load accounts from the JSON file and check if they are live."""
        log_event("LiveChecker: Starting the live check loop.")
        accounts = load_accounts()
        for account in accounts:
            username = account.get("tiktok_account")
            if not username:
                log_event("LiveChecker: Skipping an account with no username.")
                continue

            log_event(f"LiveChecker: Checking live status for account '{username}'.")

            if username not in self.clients:
                # Initialize a new client for the username
                client = TikTokLiveClient(unique_id=username)
                self.clients[username] = client

            client = self.clients[username]

            try:
                # Check if the user is live
                if not await client.is_live():
                    log_event(f"LiveChecker: Account '{username}' is not live.")
                    update_account(tiktok_account=username, online=False, last_checked=self.get_current_time())
                else:
                    log_event(f"LiveChecker: Account '{username}' is live.")
                    update_account(
                        tiktok_account=username,
                        online=True,
                        last_online=self.get_current_time(),
                        last_checked=self.get_current_time()
                    )
                    new_live_signal.emit(username)  # Emit signal for new live account
                    play_alert_sound()
                    notification.notify(title="TikToker Live Alert", message=f"{username}", timeout=5)
            except Exception as e:
                # Log the error and continue with the next account
                log_event(f"LiveChecker: Error checking live status for '{username}': {str(e)}")
                update_account(tiktok_account=username, online=False, last_checked=self.get_current_time())

        log_event("LiveChecker: Completed a live check cycle.")
        await asyncio.sleep(interval * 60)

    def get_current_time(self):
        """Get the current time in ISO 8601 format."""
        return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    async def on_connect(self, event: ConnectEvent):
        """Handle the connect event."""
        log_event(f"LiveChecker: Connected to TikTok live stream for user: {event.client.unique_id}")
        print(f"Connected to TikTok live stream for user: {event.client.unique_id}")

    async def on_comment(self, event: CommentEvent):
        """Handle the comment event."""
        log_event(f"LiveChecker: Comment from {event.user.nickname}: {event.comment}")
        print(f"Comment from {event.user.nickname}: {event.comment}")

    def stop(self):
        """Stop the live checker loop."""
        log_event("LiveChecker: Stopping the live check loop.")
        self.running = False