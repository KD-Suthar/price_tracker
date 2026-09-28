"""
MongoDB Atlas-backed implementation of PriceStore (works on the free M0 tier).

Collections:
  price_history  -- one document per PricePoint
  alert_log      -- one document per AlertEvent (rule is embedded)

Note on the free tier: M0 has a 512 MB storage cap, so a TTL index on
`fetched_at` (see ensure_indexes) keeps old price points from filling it up.
"""
from pymongo import MongoClient, DESCENDING
from price_tracker.config import settings
from price_tracker.models import PricePoint, AlertEvent, AlertRule
from price_tracker.storage.base import PriceStore


class MongoStore(PriceStore):
    def __init__(self, client: MongoClient | None = None):
        # `client` is injectable so tests can pass a mongomock client.
        self.client = client or MongoClient(settings.mongodb_uri, serverSelectionTimeoutMS=5000)
        self.db = self.client[settings.mongodb_db]
        self.prices = self.db["price_history"]
        self.alerts = self.db["alert_log"]
        self.ensure_indexes()

    def ensure_indexes(self) -> None:
        """Idempotent -- safe to call on every startup."""
        self.prices.create_index([("symbol", 1), ("fetched_at", DESCENDING)])
        self.prices.create_index(
            "fetched_at",
            expireAfterSeconds=settings.price_ttl_days * 24 * 3600,
            name="fetched_at_ttl",
        )
        self.alerts.create_index([("triggered_at", DESCENDING)])

    def save_price(self, price: PricePoint) -> None:
        self.prices.insert_one(price.model_dump())

    def get_price_history(self, symbol: str, limit: int = 100) -> list[PricePoint]:
        cursor = (
            self.prices.find({"symbol": symbol}, {"_id": 0})
            .sort("fetched_at", DESCENDING)
            .limit(limit)
        )
        return [PricePoint(**doc) for doc in cursor]

    def save_alert_event(self, event: AlertEvent) -> None:
        self.alerts.insert_one(event.model_dump())

    def get_alert_log(self, limit: int = 100) -> list[AlertEvent]:
        cursor = self.alerts.find({}, {"_id": 0}).sort("triggered_at", DESCENDING).limit(limit)
        events = []
        for doc in cursor:
            doc["rule"] = AlertRule(**doc["rule"])
            events.append(AlertEvent(**doc))
        return events
