# Architecture

```
                 +----------------+   +----------------+
                 | CoinGeckoClient|   |AlphaVantageClient|
                 +-------+--------+   +--------+---------+
                         |  (Exchange interface)|
                         v                      v
                     +-------------------------------+
                     |         PriceFetcher          |
                     |  (ThreadPoolExecutor, concurrent
                     |   fetch across all exchanges)  |
                     +---------------+----------------+
                                     |
                          PricePoint (pydantic model)
                                     |
                 +-------------------+-------------------+
                 |                                       |
                 v                                       v
       +------------------+                    +-------------------+
       |   PriceStore      |                    |   rules.evaluate  |
       | (MongoDB Atlas)|                   | (AlertRule check) |
       +------------------+                    +----------+---------+
                 ^                                         |
                 |                                    AlertEvent
                 |                                         v
                 |                              +-----------------+
                 +------------------------------|   Notifier      |
                        (log alert too)          | (console/email/ |
                                                  |  telegram)      |
                                                  +-----------------+

Scheduler (APScheduler) drives PriceFetcher -> rules.evaluate -> Notifier
on a fixed interval. Optional Streamlit dashboard reads from PriceStore
independently of the polling loop.
```

## Component responsibilities

- **exchanges/**: one class per data source, all implementing `Exchange.get_price`.
  Adding a new source never touches the fetcher, storage, or alert code.
- **fetcher.py**: fans out `get_price` calls across a thread pool; isolates
  one exchange's failure from the others.
- **models.py**: the only schema every other component agrees on
  (`PricePoint`, `AlertRule`, `AlertEvent`).
- **storage/**: `PriceStore` interface with a MongoDB Atlas implementation (free M0 tier).
  A TTL index on `fetched_at` keeps history within the 512 MB free-tier cap.
- **alerts/**: `rules.evaluate` is pure logic (easy to unit test); notifiers are
  swappable delivery channels behind `Notifier`.
- **scheduler.py + cli.py**: wires everything together and runs it forever.
- **dashboard/app.py**: optional, reads from the same `PriceStore` -- decoupled
  from the polling loop entirely.
