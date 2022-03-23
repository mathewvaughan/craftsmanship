from babel.numbers import format_currency

def statement(invoice, plays):
    total_amount=0
    volume_credits=0
    result = f"Statement for {invoice['customer']}\n"
    format = lambda x : format_currency(x, 'USD', locale='en_US')
    for perf in invoice["performances"]:
        play = plays[perf["playID"]]
        this_amount = amount_for(perf, play)
        # Add volume credits
        volume_credits+=max(perf['audience']-30,0)
        # add extra credit for every ten comedy attendees
        if play["type"] == "comedy":
            volume_credits += int(perf["audience"]/5)
        result +=f"  {play['name']} : {format(this_amount/100)} ({perf['audience']} seats)\n"
        total_amount += this_amount
    result+= f"Amount owed is {format(total_amount/100)}\n"
    result+= f"You earned {volume_credits} credits\n"
    return result

def amount_for(perf, play):
    result=0
    if play["type"] == "tragedy":
        result=40000
        if perf["audience"] > 30:
            result += 1000*(perf['audience']-30)
    elif play["type"] == "comedy":
        result = 30000
        if perf["audience"] > 20:
            result +=10000+500*(perf['audience'] - 20)
        result += 300 * perf["audience"]
    if play["type"] not in {"tragedy", "comedy"}:
        raise ValueError("Unknown Play type: %s".format(play["type"]))
    return result
