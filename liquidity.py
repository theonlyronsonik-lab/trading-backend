def liquidity_sweep_level(candles, direction):
    if direction == "bullish":
        return float(candles[-1]["low"])
    else:
        return float(candles[-1]["high"])
