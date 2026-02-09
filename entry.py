from data import get_candles


# ==============================
# MARKET STRUCTURE (LTF)
# ==============================
def detect_market_structure(candles, bias):
    """
    Confirms simple pullback + continuation structure
    """

    if len(candles) < 20:
        return False

    last = candles[-1]
    prev = candles[-2]

    if bias == "BULLISH":
        return last["close"] > prev["high"]

    if bias == "BEARISH":
        return last["close"] < prev["low"]

    return False


# ==============================
# ENTRY LOGIC
# ==============================
def find_ltf_entry(symbol, bias):
    candles = get_candles(symbol, interval="15min", limit=50)

    if not candles:
        return None

    structure_ok = detect_market_structure(candles, bias)
    if not structure_ok:
        return None

    entry_price = candles[-1]["close"]

    if bias == "BULLISH":
        sl = min(c["low"] for c in candles[-10:])
        tp = entry_price + 3 * (entry_price - sl)

    else:
        sl = max(c["high"] for c in candles[-10:])
        tp = entry_price - 3 * (sl - entry_price)

    risk = abs(entry_price - sl)
    reward = abs(tp - entry_price)

    if risk == 0:
        return None

    rr = round(reward / risk, 2)

    if rr < 3:
        return None

    return {
        "entry": round(entry_price, 5),
        "sl": round(sl, 5),
        "tp": round(tp, 5),
        "rr": rr,
    }
