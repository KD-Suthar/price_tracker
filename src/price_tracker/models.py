"""
Pydantic models shared across exchanges, storage, and alerts.
Keeping these separate from any one exchange's API shape means every
downstream component (storage, alerts, dashboard) only ever deals with
one clean, validated schema regardless of which exchange the data came from.
"""
from datetime import datetime
from pydantic import BaseModel, Field


class PricePoint(BaseModel):
    symbol: str
    price: float
    currency: str = "USD"
    source: str                       # e.g. "coingecko", "alpha_vantage"
    fetched_at: datetime = Field(default_factory=datetime.utcnow)


class AlertRule(BaseModel):
    symbol: str
    condition: str                    # "above" | "below" | "pct_change"
    threshold: float
    active: bool = True


class AlertEvent(BaseModel):
    symbol: str
    rule: AlertRule
    triggered_price: float
    triggered_at: datetime = Field(default_factory=datetime.utcnow)
    message: str
