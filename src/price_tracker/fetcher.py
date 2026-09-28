"""
Orchestrates concurrent fetches across all configured exchanges using a
thread pool -- these are I/O-bound calls (waiting on network), so threads
give a real speedup here without needing asyncio.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from price_tracker.exchanges.base import Exchange
from price_tracker.models import PricePoint


class PriceFetcher:
    def __init__(self, exchanges: list[Exchange], max_workers: int = 4):
        self.exchanges = exchanges
        self.max_workers = max_workers

    def fetch_all(self, symbol: str) -> list[PricePoint]:
        """Fetch `symbol` from every configured exchange concurrently.
        A failure in one exchange must not block the others -- collect
        successes, log/skip failures."""
        results: list[PricePoint] = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
            futures = {
                pool.submit(ex.get_price, symbol): ex for ex in self.exchanges
            }
            for future in as_completed(futures):
                exchange = futures[future]
                try:
                    results.append(future.result())
                except Exception as exc:  # noqa: BLE001
                    # TODO: structured logging instead of print
                    print(f"[{exchange.name}] failed for {symbol}: {exc}")
        return results
