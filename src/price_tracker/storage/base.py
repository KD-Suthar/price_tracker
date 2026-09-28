"""
Abstract storage interface. The rest of the app (fetcher, alerts, CLI,
dashboard) depends only on this interface -- swapping MongoDB for
any other backend should never require touching business logic.
"""
from abc import ABC, abstractmethod
from price_tracker.models import PricePoint, AlertEvent


class PriceStore(ABC):
    @abstractmethod
    def save_price(self, price: PricePoint) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_price_history(self, symbol: str, limit: int = 100) -> list[PricePoint]:
        raise NotImplementedError

    @abstractmethod
    def save_alert_event(self, event: AlertEvent) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_alert_log(self, limit: int = 100) -> list[AlertEvent]:
        raise NotImplementedError
