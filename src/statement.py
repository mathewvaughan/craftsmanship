from babel.numbers import format_currency
from copy import copy

def statement(invoice, plays):
    return plain_text(statement_data(invoice, plays))

def statement_data(invoice, plays):
    def play_for(performance):
        return plays[performance["playID"]]

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

    def enrich_performance(performance):
        result = copy(performance)
        result["play"] = play_for(result)
        result["amount"] = amount_for(result)
        result["credits"] = volume_credits_for(result)
        return result
    
    def total_volume_credits(data):
        volume_credits=0
        for performance in data["performances"]:
            volume_credits+=performance["credits"]
        return volume_credits
    
    def total_amount(data):
        result=0
        for performance in data["performances"]:
            result += performance["amount"]
        return result

    result={
        "customer": invoice["customer"],
        "performances": [enrich_performance(performance) for performance in invoice["performances"]]
    }
    result["total_amount"] = total_amount(result)
    result["total_credits"] = total_volume_credits(result)
    return result

def plain_text(data):
    usd = lambda x : format_currency(x, 'USD', locale='en_US')
    result = f"Statement for {data['customer']}\n"
    for perf in data["performances"]:
        result +=f"  {perf['play']['name']} : {usd(perf['amount']/100)} ({perf['audience']} seats)\n"
    result+= f"Amount owed is {usd(data['total_amount']/100)}\n"
    result+= f"You earned {data['total_credits']} credits\n"
    return result


