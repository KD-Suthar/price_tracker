"""
MongoStore tests run against mongomock (an in-memory fake), so no Atlas
connection or credentials are needed in CI.
"""
from datetime import datetime, timedelta
import mongomock
from price_tracker.models import PricePoint, AlertRule, AlertEvent
from price_tracker.storage.mongo_store import MongoStore


def make_store() -> MongoStore:
    return MongoStore(client=mongomock.MongoClient())


def test_save_and_read_price_history():
    store = make_store()
    # Explicit timestamps: Mongo stores millisecond precision, so two
    # back-to-back utcnow() calls can tie.
    t0 = datetime.utcnow() - timedelta(minutes=5)  # recent, so the TTL index does not expire it
    store.save_price(PricePoint(symbol="BTC", price=65000.0, source="test", fetched_at=t0))
    store.save_price(
        PricePoint(symbol="BTC", price=65100.0, source="test", fetched_at=t0 + timedelta(minutes=1))
    )
    history = store.get_price_history("BTC")
    assert len(history) == 2
    assert history[0].price == 65100.0  # newest first


def test_alert_event_roundtrip():
    store = make_store()
    rule = AlertRule(symbol="BTC", condition="above", threshold=60000)
    store.save_alert_event(
        AlertEvent(symbol="BTC", rule=rule, triggered_price=65000, message="BTC above 60000")
    )
    log = store.get_alert_log()
    assert len(log) == 1
    assert log[0].rule.threshold == 60000
