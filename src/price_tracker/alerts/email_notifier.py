"""
Sends alert events via SMTP. Minimal by design -- swap in a transactional
email provider's API later if deliverability becomes a real concern.
"""
import smtplib
from email.message import EmailMessage
from price_tracker.config import settings
from price_tracker.models import AlertEvent
from price_tracker.alerts.notifier_base import Notifier


class EmailNotifier(Notifier):
    def send(self, event: AlertEvent) -> None:
        msg = EmailMessage()
        msg["Subject"] = f"Price Alert: {event.symbol}"
        msg["From"] = settings.smtp_user if hasattr(settings, "smtp_user") else ""
        msg["To"] = ""  # TODO: read ALERT_EMAIL_TO from settings
        msg.set_content(event.message)

        # TODO: wrap in try/except, log failures, don't crash the poll loop
        with smtplib.SMTP(settings.smtp_host if hasattr(settings, "smtp_host") else "", 587) as server:
            server.starttls()
            server.login(settings.smtp_user, settings.smtp_password)
            server.send_message(msg)
