"""
Evaluates a symbol's latest price against its active AlertRules and
produces AlertEvents for anything that fired. Pure logic, no I/O --
easy to unit test in isolation from storage/notifiers.
"""
from price_tracker.models import AlertRule, AlertEvent


def evaluate(symbol: str, current_price: float, rules: list[AlertRule]) -> list[AlertEvent]:
    events: list[AlertEvent] = []
    for rule in rules:
        if not rule.active or rule.symbol != symbol:
            continue

        fired = False
        if rule.condition == "above" and current_price > rule.threshold:
            fired = True
        elif rule.condition == "below" and current_price < rule.threshold:
            fired = True
        elif rule.condition == "pct_change":
            # TODO: needs previous price from storage to compute % change
            pass

        if fired:
            events.append(
                AlertEvent(
                    symbol=symbol,
                    rule=rule,
                    triggered_price=current_price,
                    message=f"{symbol} {rule.condition} {rule.threshold} (now {current_price})",
                )
            )
    return events
