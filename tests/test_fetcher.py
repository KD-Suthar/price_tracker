"""
Tests that PriceFetcher tolerates one exchange failing without losing
results from the others -- this is the behavior threading is there for.
"""
from price_tracker.exchanges.base import Exchange
from price_tracker.models import PricePoint
from price_tracker.fetcher import PriceFetcher


class GoodExchange(Exchange):
    name = "good"

    def get_price(self, symbol: str) -> PricePoint:
        return PricePoint(symbol=symbol, price=100.0, source=self.name)


class FailingExchange(Exchange):
    name = "failing"

    def get_price(self, symbol: str) -> PricePoint:
        raise RuntimeError("simulated API failure")


def test_fetch_all_tolerates_partial_failure():
    fetcher = PriceFetcher([GoodExchange(), FailingExchange()])
    results = fetcher.fetch_all("BTC")
    assert len(results) == 1
    assert results[0].source == "good"
