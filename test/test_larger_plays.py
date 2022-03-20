from src.statement import statement

def test_large_audience_tragedy(plays):
    invoice = {
            "customer": "BigCo",
            "performances": [
                {"playID": "hamlet", "audience": 31},
            ]
        }
    assert statement(invoice, plays) == "Statement for BigCo\n" \
    "  Hamlet : $410.00 (31 seats)\n" \
    "Amount owed is $410.00\n" \
    "You earned 1 credits\n"

def test_large_audience_comedy(plays):
    invoice = {
            "customer": "BigCo",
            "performances": [
                {"playID": "as-like", "audience": 21},
            ]
        }
    assert statement(invoice, plays) == "Statement for BigCo\n" \
    "  As You Like It : $468.00 (21 seats)\n" \
    "Amount owed is $468.00\n" \
    "You earned 4 credits\n"
