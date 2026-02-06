# risk.py

def calculate_levels(candles, direction, rr):
    last = candles[-1]["close"]

    if direction == "BUY":
        sl = min(c["low"] for c in candles[-10:])
        tp = last + (last - sl) * rr

    elif direction == "SELL":
        sl = max(c["high"] for c in candles[-10:])
        tp = last - (sl - last) * rr

    else:
        return None

    return {
        "entry": round(last, 2),
        "sl": round(sl, 2),
        "tp": round(tp, 2),
    }
