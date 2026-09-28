# Price Tracker & Alert Engine

Tracks prices for a watchlist of stocks/crypto across multiple APIs, persists history
to a cloud database, and fires alerts when a price crosses a user-defined threshold.

## Why this exists
A small, end-to-end system that mirrors a real ingest -> store -> serve pipeline:
concurrent fetching from multiple sources, validated data models, a swappable storage
backend, rule-based alerting, and an optional dashboard.

## Features
- Pluggable exchange clients (CoinGecko, Alpha Vantage, ...) behind a common interface
- Concurrent fetching via a thread pool (I/O-bound API calls)
- Cloud-backed persistence on MongoDB Atlas (free M0 tier) behind a common storage interface
- Rule-based alerting (price above/below/percent-change) with pluggable notifiers
  (console, email, Telegram)
- Scheduled polling (APScheduler)
- Optional Streamlit dashboard for price history + alert log

## MongoDB Atlas setup (free tier)
1. Create a free **M0** cluster at cloud.mongodb.com
2. Database Access -> add a database user (username + password)
3. Network Access -> allow your IP (or `0.0.0.0/0` for local dev only)
4. Connect -> Drivers -> copy the `mongodb+srv://...` string into `MONGODB_URI` in `.env`

M0 caps storage at 512 MB, so price history uses a TTL index
(`PRICE_TTL_DAYS`, default 30) and old points expire automatically.

## Architecture

See [docs/architecture.md](docs/architecture.md) for the data flow diagram and
component responsibilities.

## Getting started

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in API keys + your Atlas connection string
python scripts/init_indexes.py   # verify the Atlas connection + create indexes
python -m price_tracker.cli run
```
