def detect_swings(candles, lookback=3):
    swings = {"highs": [], "lows": []}

    for i in range(lookback, len(candles) - lookback):
        high = candles[i]["high"]
        low = candles[i]["low"]

        if high == max(c["high"] for c in candles[i-lookback:i+lookback+1]):
            swings["highs"].append((i, high))

        if low == min(c["low"] for c in candles[i-lookback:i+lookback+1]):
            swings["lows"].append((i, low))

    return swings


def detect_market_structure(candles):
    swings = detect_swings(candles)

    if len(swings["highs"]) < 2 or len(swings["lows"]) < 2:
        return None

    last_high = swings["highs"][-1][1]
    prev_high = swings["highs"][-2][1]

    last_low = swings["lows"][-1][1]
    prev_low = swings["lows"][-2][1]

    last_close = candles[-1]["close"]

    if last_close > prev_high:
        return {
            "bias": "Bullish",
            "BOS": "Break above previous high"
        }

    if last_close < prev_low:
        return {
            "bias": "Bearish",
            "BOS": "Break below previous low"
        }

    return {
        "bias": "Range",
        "BOS": "No valid break"
    }
