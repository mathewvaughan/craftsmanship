from src.statement import statement

def test_multiple_plays(plays):
    invoice = {
            "customer": "BigCo",
            "performances": [
                {"playID": "hamlet", "audience": 30},
                {"playID": "as-like", "audience": 21}
            ]
        }
    assert statement(invoice, plays) == "Statement for BigCo\n" \
    "  Hamlet : $400.00 (30 seats)\n" \
    "  As You Like It : $468.00 (21 seats)\n" \
    "Amount owed is $868.00\n" \
    "You earned 4 credits\n"

