"""
Abstract base class every exchange client implements. This is the seam
that lets the fetcher treat CoinGecko, Alpha Vantage, or any future
source identically -- add a new subclass, no other code changes.
"""
from abc import ABC, abstractmethod
from price_tracker.models import PricePoint


class Exchange(ABC):
    name: str = "base"

    @abstractmethod
    def get_price(self, symbol: str) -> PricePoint:
        """Fetch the current price for a single symbol. Must raise on failure,
        never return a silently-wrong value -- the fetcher decides how to
        handle a failed source (skip, retry, alert on staleness)."""
        raise NotImplementedError
