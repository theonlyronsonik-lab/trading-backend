def find_fvg(candles, bias):
    """
    Detect simple 3-candle Fair Value Gap
    """
    if len(candles) < 5:
        return None

    c1, c2, c3 = candles[-3], candles[-2], candles[-1]

    if bias == "BULLISH":
        if c1["high"] < c3["low"]:
            return {
                "type": "BULLISH_FVG",
                "low": c1["high"],
                "high": c3["low"]
            }

    if bias == "BEARISH":
        if c1["low"] > c3["high"]:
            return {
                "type": "BEARISH_FVG",
                "high": c1["low"],
                "low": c3["high"]
            }

    return None


def candle_confirmation(candle, bias):
    """
    Simple confirmation candle
    """
    body = abs(candle["close"] - candle["open"])
    wick = candle["high"] - candle["low"]

    if wick == 0:
        return False

    strength = body / wick

    if strength < 0.5:
        return False

    if bias == "BULLISH" and candle["close"] > candle["open"]:
        return True

    if bias == "BEARISH" and candle["close"] < candle["open"]:
        return True

    return False
