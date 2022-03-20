from src.statement import statement

def test_large_audience_tragedy(plays):
    invoice = {
            "customer": "SmallCo",
            "performances": [
                {"playID": "hamlet", "audience": 31},
            ]
        }
    assert statement(invoice, plays) == "Statement for SmallCo\n" \
    "  Hamlet : $410.00 (31 seats)\n" \
    "Amount owed is $410.00\n" \
    "You earned 1 credits\n"