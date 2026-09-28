"""
Alpha Vantage client -- free tier, API key required, good for stock symbols.
"""
import requests
from price_tracker.config import settings
from price_tracker.exchanges.base import Exchange
from price_tracker.models import PricePoint

ALPHA_VANTAGE_URL = "https://www.alphavantage.co/query"


class AlphaVantageClient(Exchange):
    name = "alpha_vantage"

    def get_price(self, symbol: str) -> PricePoint:
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": settings.alpha_vantage_api_key,
        }
        resp = requests.get(ALPHA_VANTAGE_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        # TODO: handle rate-limit / error payloads Alpha Vantage returns with HTTP 200
        price = float(data["Global Quote"]["05. price"])
        return PricePoint(symbol=symbol, price=price, source=self.name)
