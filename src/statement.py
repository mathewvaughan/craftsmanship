from babel.numbers import format_currency

def statement(invoice, plays):
    return plain_text(invoice, plays)

def plain_text(invoice, plays):
    usd = lambda x : format_currency(x, 'USD', locale='en_US')

    def play_for(performance):
        return plays[performance["playID"]]

    def amount_for(performance):
        result=0
        if play_for(performance)["type"] == "tragedy":
            result=40000
            if performance["audience"] > 30:
                result += 1000*(performance['audience']-30)
        elif play_for(performance)["type"] == "comedy":
            result = 30000
            if performance["audience"] > 20:
                result +=10000+500*(performance['audience'] - 20)
            result += 300 * performance["audience"]
        if play_for(performance)["type"] not in {"tragedy", "comedy"}:
            raise ValueError("Unknown Play type: %s".format(play_for(performance)["type"]))
        return result

    def volume_credits_for(performance):
        result = max(performance['audience']-30,0)
        if play_for(performance)["type"] == "comedy":
            result += int(performance["audience"]/5)
        return result

    def total_volume_credits():
        volume_credits=0
        for performance in invoice["performances"]:
            volume_credits+=volume_credits_for(performance)
        return volume_credits
    
    def total_amount():
        result=0
        for performance in invoice["performances"]:
            result += amount_for(performance)
        return result

    result = f"Statement for {invoice['customer']}\n"
    for perf in invoice["performances"]:
        result +=f"  {play_for(perf)['name']} : {usd(amount_for(perf)/100)} ({perf['audience']} seats)\n"
    result+= f"Amount owed is {usd(total_amount()/100)}\n"
    result+= f"You earned {total_volume_credits()} credits\n"
    return result


