"""
One-off script: connects to Atlas and creates the indexes (including the TTL
index that protects the free tier's 512 MB cap). MongoStore does this on
startup too, so this is mainly a quick way to verify your connection string.

    python scripts/init_indexes.py
"""
import sys
from pathlib import Path

# scripts/init_indexes.py -> parent = scripts/ -> parent.parent = repo root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))


from price_tracker.storage.mongo_store import MongoStore


def main() -> None:
    store = MongoStore()
    store.client.admin.command("ping")
    print("Connected to Atlas. Indexes ensured on:", store.db.name)


if __name__ == "__main__":
    main()
