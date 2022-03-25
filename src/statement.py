from babel.numbers import format_currency
from copy import copy

def statement(invoice, plays):
    def play_for(performance):
        return plays[performance["playID"]]

    def enrich_performance(performance):
        result = copy(performance)
        result["play"] = play_for(performance)
        return result

    statement_data={
        "customer": invoice["customer"],
        "performances": [enrich_performance(performance) for performance in invoice["performances"]]
    }

    return plain_text(statement_data)

def plain_text(data):
    usd = lambda x : format_currency(x, 'USD', locale='en_US')

    def amount_for(performance):
        result=0
        if performance["play"]["type"] == "tragedy":
            result=40000
            if performance["audience"] > 30:
                result += 1000*(performance['audience']-30)
        elif performance["play"]["type"] == "comedy":
            result = 30000
            if performance["audience"] > 20:
                result +=10000+500*(performance['audience'] - 20)
            result += 300 * performance["audience"]
        if performance["play"]["type"] not in {"tragedy", "comedy"}:
            raise ValueError("Unknown Play type: %s".format(performance["play"]["type"]))
        return result

    def volume_credits_for(performance):
        result = max(performance['audience']-30,0)
        if performance["play"]["type"] == "comedy":
            result += int(performance["audience"]/5)
        return result

    def total_volume_credits():
        volume_credits=0
        for performance in data["performances"]:
            volume_credits+=volume_credits_for(performance)
        return volume_credits
    
    def total_amount():
        result=0
        for performance in data["performances"]:
            result += amount_for(performance)
        return result

    result = f"Statement for {data['customer']}\n"
    for perf in data["performances"]:
        result +=f"  {perf['play']['name']} : {usd(amount_for(perf)/100)} ({perf['audience']} seats)\n"
    result+= f"Amount owed is {usd(total_amount()/100)}\n"
    result+= f"You earned {total_volume_credits()} credits\n"
    return result


