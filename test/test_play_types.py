import pytest
from src.statement import statement
# In the digital age, frailty's name is software - Martin Fowler


def test_small_audience_tragedy(plays):
    invoice = {
            "customer": "BigCo",
            "performances": [
                {"playID": "hamlet", "audience": 20},
            ]
        }
    x  = statement(invoice, plays)
    assert x == "Statement for BigCo\n" \
    "  Hamlet : $400.00 (20 seats)\n" \
    "Amount owed is $400.00\n" \
    "You earned 0 credits\n"


def test_small_audience_comedy(plays):
    invoice = {
            "customer": "BigCo",
            "performances": [
                {"playID": "as-like", "audience": 15},
            ]
        }
    x  = statement(invoice, plays)
    assert x == "Statement for BigCo\n" \
    "  As You Like It : $345.00 (15 seats)\n" \
    "Amount owed is $345.00\n" \
    "You earned 3 credits\n"

def test_unknown_play_type(plays):
    invoice = {
            "customer": "BigCo",
            "performances": [
                {"playID": "BAD_PLAY", "audience": 15},
            ]
        }
    bad_plays = {
        **plays,
        "BAD_PLAY": {"name": "BAD PLAY", "type": "Postmodern Interpretive Slam Poetry Dance"},
    }
    with pytest.raises(ValueError):
        x  = statement(invoice, bad_plays)