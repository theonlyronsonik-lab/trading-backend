from data import get_candles
from config import LOOKBACK_LTF, RR_RATIO


def find_ltf_entry(symbol, bias, timeframe):
    candles = get_candles(symbol, timeframe, limit=LOOKBACK_LTF)

    if not candles or len(candles) < 50:
        return None

    highs = [c["high"] for c in candles]
    lows = [c["low"] for c in candles]
    closes = [c["close"] for c in candles]

    # -------------------------
    # 1. Detect BOS
    # -------------------------
    recent_high = max(highs[-20:-5])
    recent_low = min(lows[-20:-5])
    last_close = closes[-1]

    if bias == "BULLISH" and last_close <= recent_high:
        return None

    if bias == "BEARISH" and last_close >= recent_low:
        return None

    # -------------------------
    # 2. Detect CHoCH (simple)
    # -------------------------
    prev_high = highs[-10]
    prev_low = lows[-10]

    if bias == "BULLISH" and prev_low < lows[-20]:
        return None

    if bias == "BEARISH" and prev_high > highs[-20]:
        return None

    # -------------------------
    # 3. Define Supply / Demand
    # -------------------------
    if bias == "BULLISH":
        zone_low = min(lows[-15:])
        zone_high = max(lows[-15:])
        entry = (zone_low + zone_high) / 2
        sl = zone_low
        tp = entry + (entry - sl) * RR_RATIO

    else:  # BEARISH
        zone_high = max(highs[-15:])
        zone_low = min(highs[-15:])
        entry = (zone_low + zone_high) / 2
        sl = zone_high
        tp = entry - (sl - entry) * RR_RATIO

    return {
        "entry_zone": f"{round(zone_low, 5)} → {round(zone_high, 5)}",
        "entry": round(entry, 5),
        "sl": round(sl, 5),
        "tp": round(tp, 5),
    }
