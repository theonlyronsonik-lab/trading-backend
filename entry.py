# entry.py

def confirm_entry(bias, liquidity):
    if bias == "BULLISH" and liquidity == "SELL_SIDE":
        return "BUY"

    if bias == "BEARISH" and liquidity == "BUY_SIDE":
        return "SELL"

    return None

