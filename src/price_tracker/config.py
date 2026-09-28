"""
Central config loader. Reads from .env via python-dotenv and exposes
typed settings so the rest of the app never touches os.environ directly.
"""
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    poll_interval_seconds: int = int(os.getenv("POLL_INTERVAL_SECONDS", "60"))
    notify_channel: str = os.getenv("NOTIFY_CHANNEL", "console")

    alpha_vantage_api_key: str = os.getenv("ALPHA_VANTAGE_API_KEY", "")

    mongodb_uri: str = os.getenv("MONGODB_URI", "")
    mongodb_db: str = os.getenv("MONGODB_DB", "price_tracker")
    price_ttl_days: int = int(os.getenv("PRICE_TTL_DAYS", "30"))


settings = Settings()
