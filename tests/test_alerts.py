"""
Unit tests for the pure alert-rule evaluation logic.
"""
from price_tracker.models import AlertRule
from price_tracker.alerts.rules import evaluate


def test_above_condition_fires():
    rule = AlertRule(symbol="BTC", condition="above", threshold=60000)
    events = evaluate("BTC", current_price=65000, rules=[rule])
    assert len(events) == 1
    assert events[0].triggered_price == 65000


def test_inactive_rule_does_not_fire():
    rule = AlertRule(symbol="BTC", condition="above", threshold=60000, active=False)
    events = evaluate("BTC", current_price=65000, rules=[rule])
    assert len(events) == 0
