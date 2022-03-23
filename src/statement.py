from babel.numbers import format_currency

def statement(invoice, plays):
    total_amount=0
    volume_credits=0

    result = f"Statement for {invoice['customer']}\n"
    usd = lambda x : format_currency(x, 'USD', locale='en_US')

    def play_for(perf):
        return plays[perf["playID"]]

    def amount_for(performance):
        result=0
        if play_for(perf)["type"] == "tragedy":
            result=40000
            if performance["audience"] > 30:
                result += 1000*(performance['audience']-30)
        elif play_for(perf)["type"] == "comedy":
            result = 30000
            if performance["audience"] > 20:
                result +=10000+500*(performance['audience'] - 20)
            result += 300 * performance["audience"]
        if play_for(perf)["type"] not in {"tragedy", "comedy"}:
            raise ValueError("Unknown Play type: %s".format(play_for(perf)["type"]))
        return result

    def volume_credits_for(perf):
        result = max(perf['audience']-30,0)
        if play_for(perf)["type"] == "comedy":
            result += int(perf["audience"]/5)
        return result
    
    for perf in invoice["performances"]:
        volume_credits+=volume_credits_for(perf)
        result +=f"  {play_for(perf)['name']} : {usd(amount_for(perf)/100)} ({perf['audience']} seats)\n"
        total_amount += amount_for(perf)
    result+= f"Amount owed is {usd(total_amount/100)}\n"
    result+= f"You earned {volume_credits} credits\n"
    return result
