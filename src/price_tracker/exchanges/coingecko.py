"""
CoinGecko client -- free, no API key required. Good default source for crypto symbols.
"""
import requests
from price_tracker.exchanges.base import Exchange
from price_tracker.models import PricePoint

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"


class CoinGeckoClient(Exchange):
    name = "coingecko"

    def get_price(self, symbol: str) -> PricePoint:
        # TODO: map friendly symbols (e.g. "BTC") to CoinGecko ids (e.g. "bitcoin")
        params = {"ids": symbol, "vs_currencies": "usd"}
        resp = requests.get(COINGECKO_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        price = data[symbol]["usd"]
        return PricePoint(symbol=symbol, price=price, source=self.name)
