"""
Unit tests for exchange clients -- mock the HTTP layer so tests don't
depend on real network calls or API keys.
"""
from unittest.mock import patch, MagicMock
from price_tracker.exchanges.coingecko import CoinGeckoClient


def test_coingecko_get_price():
    fake_response = MagicMock()
    fake_response.json.return_value = {"bitcoin": {"usd": 65000.0}}
    fake_response.raise_for_status.return_value = None

    with patch("requests.get", return_value=fake_response):
        client = CoinGeckoClient()
        result = client.get_price("bitcoin")

    assert result.price == 65000.0
    assert result.source == "coingecko"
