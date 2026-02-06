def confirm_entry(bias, candles):
    """
    candles: LTF candles (most recent first or last — we handle both)
    returns dict with entry zone, SL, TP
    """

    # Ensure candles are ordered oldest → newest
    candles = list(reversed(candles))

    highs = [float(c["high"]) for c in candles]
    lows = [float(c["low"]) for c in candles]
    closes = [float(c["close"]) for c in candles]

    recent_high = max(highs[-20:])
    recent_low = min(lows[-20:])

    current_price = closes[-1]

    if bias == "BULLISH":
        entry_zone = (
            round(recent_low + (recent_high - recent_low) * 0.5, 2),
            round(recent_low + (recent_high - recent_low) * 0.62, 2),
        )
        stop_loss = round(recent_low - 0.2, 2)
        risk = entry_zone[1] - stop_loss
        take_profit = round(entry_zone[1] + risk * 2, 2)

    elif bias == "BEARISH":
        entry_zone = (
            round(recent_high - (recent_high - recent_low) * 0.62, 2),
            round(recent_high - (recent_high - recent_low) * 0.5, 2),
        )
        stop_loss = round(recent_high + 0.2, 2)
        risk = stop_loss - entry_zone[0]
        take_profit = round(entry_zone[0] - risk * 2, 2)

    else:
        return None

    return {
        "zone": entry_zone,
        "sl": stop_loss,
        "tp": take_profit,
    }
