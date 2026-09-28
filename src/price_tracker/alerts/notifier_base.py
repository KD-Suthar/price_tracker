"""
Abstract notifier interface -- console, email, Telegram, whatever comes
next, all implement `send`. The alert engine doesn't know or care which.
"""
from abc import ABC, abstractmethod
from price_tracker.models import AlertEvent


class Notifier(ABC):
    @abstractmethod
    def send(self, event: AlertEvent) -> None:
        raise NotImplementedError


class ConsoleNotifier(Notifier):
    def send(self, event: AlertEvent) -> None:
        print(f"[ALERT] {event.message}")
