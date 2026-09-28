"""
Sends alert events via a Telegram bot -- often the fastest notifier to
set up for a personal project (no domain, no SMTP config, just a token).
"""
import requests
from price_tracker.models import AlertEvent
from price_tracker.alerts.notifier_base import Notifier


class TelegramNotifier(Notifier):
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id

    def send(self, event: AlertEvent) -> None:
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        resp = requests.post(url, data={"chat_id": self.chat_id, "text": event.message}, timeout=10)
        resp.raise_for_status()
