import argparse

from price_tracker.alerts.notifier_base import ConsoleNotifier, Notifier
from price_tracker.alerts.rules import evaluate
from price_tracker.exchanges.coingecko import CoinGeckoClient
from price_tracker.fetcher import PriceFetcher
from price_tracker.models import AlertRule
from price_tracker.scheduler import run_forever
from price_tracker.storage.base import PriceStore
from price_tracker.storage.mongo_store import MongoStore


def parse_rule(text: str) -> AlertRule:
    """'bitcoin:above:60000' -> AlertRule(symbol='bitcoin', condition='above', threshold=60000)"""
    symbol, condition, threshold = text.split(":")
    if condition not in ("above", "below"):
        raise ValueError(f"condition must be 'above' or 'below', got '{condition}'")
    return AlertRule(symbol=symbol, condition=condition, threshold=float(threshold))


def make_poll_job(
    fetcher: PriceFetcher, store: PriceStore, rules: list[AlertRule], notifier: Notifier
):
    def poll_job(symbols: list[str]) -> None:
        for symbol in symbols:
            for price in fetcher.fetch_all(symbol):
                store.save_price(price)
                print(f"{price.fetched_at:%H:%M:%S}  {price.symbol}  {price.price}  ({price.source})")
                for event in evaluate(symbol, price.price, rules):
                    store.save_alert_event(event)
                    notifier.send(event)

    return poll_job


def main() -> None:
    parser = argparse.ArgumentParser(description="Price Tracker & Alert Engine")
    sub = parser.add_subparsers(dest="command", required=True)

    run_parser = sub.add_parser("run", help="Start the polling loop")
    run_parser.add_argument("--symbols", required=True, help="Comma-separated CoinGecko ids, e.g. bitcoin,ethereum")
    run_parser.add_argument("--alert", action="append", default=[], help="symbol:above|below:threshold (repeatable)")

    args = parser.parse_args()

    if args.command == "run":
        symbols = [s.strip() for s in args.symbols.split(",")]
        rules = [parse_rule(a) for a in args.alert]

        store = MongoStore()
        fetcher = PriceFetcher([CoinGeckoClient()])
        job = make_poll_job(fetcher, store, rules, ConsoleNotifier())

        print(f"Tracking {symbols} with {len(rules)} alert rule(s). Ctrl+C to stop.")
        run_forever(job, symbols)


if __name__ == "__main__":
    main()