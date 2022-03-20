import pytest
from src.statement import statement

def test_small_audience_tragedy(plays):
    invoice = {
            "customer": "BigCo",
            "performances": [
                {"playID": "hamlet", "audience": 30},
            ]
        }
    assert statement(invoice, plays) == "Statement for BigCo\n" \
    "  Hamlet : $400.00 (30 seats)\n" \
    "Amount owed is $400.00\n" \
    "You earned 0 credits\n"


def test_small_audience_comedy(plays):
    invoice = {
            "customer": "BigCo",
            "performances": [
                {"playID": "as-like", "audience": 20},
            ]
        }
    assert statement(invoice, plays) == "Statement for BigCo\n" \
    "  As You Like It : $360.00 (20 seats)\n" \
    "Amount owed is $360.00\n" \
    "You earned 4 credits\n"

def test_unknown_play_type(plays):
    invoice = {
            "customer": "BigCo",
            "performances": [
                {"playID": "BAD_PLAY", "audience": 0},
            ]
        }
    bad_plays = {
        **plays,
        "BAD_PLAY": {"name": "BAD PLAY", "type": "Postmodern Interpretive Slam Poetry Dance"},
    }
    with pytest.raises(ValueError):
        statement(invoice, bad_plays)