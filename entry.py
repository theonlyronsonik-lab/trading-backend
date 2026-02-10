import requests

# -------------------------
# HTF BIAS CHECK
# -------------------------
if recent_high > prev_high and recent_low > prev_low:
    # You probably only want one return here, not two in a row
    # return "BULLISH" if condition met, else "RANGE"
    return "BULLISH"
else:
    return "RANGE"


# -------------------------
# LTF ENTRY (CONFIRMATION)
# -------------------------
def analyse_ltf_entry(candles, htf_bias):
    if len(candles) < 60:
        return None

    highs = [float(c["high"]) for c in candles]
    lows = [float(c["low"]) for c in candles]
    closes = [float(c["close"]) for c in candles]

    last_close = closes[-1]

    # --- Supply / Demand zones ---
    supply = max(highs[-30:-5])
    demand = min(lows[-30:-5])

    # --- CHOCH / BOS confirmation ---
    prev_high = max(highs[-10:-5])
    prev_low = min(lows[-10:-5])

    # BEARISH SETUP
    if htf_bias == "BEARISH":
        # price reacts at supply and breaks structure
        if last_close < prev_low and supply > last_close:
            entry = last_close
            sl = supply
            tp = entry - 2 * (sl - entry)

            return {
                "direction": "SELL",
                "bias": htf_bias,
                "entry": round(entry, 5),
                "sl": round(sl, 5),
                "tp": round(tp, 5),
                "reason": "LTF CHOCH/BOS after reaction from supply in HTF bearish context"
            }

    # BULLISH SETUP
    if htf_bias == "BULLISH":
        if last_close > prev_high and demand < last_close:
            entry = last_close
            sl = demand
            tp = entry + 2 * (entry - sl)

            return {
                "direction": "BUY",
                "bias": htf_bias,
                "entry": round(entry, 5),
                "sl": round(sl, 5),
                "tp": round(tp, 5),
                "reason": "LTF CHOCH/BOS after reaction from demand in HTF bullish context"
            }

    return Noneimport requests

# -------------------------
# HTF BIAS CHECK
# -------------------------
if recent_high > prev_high and recent_low > prev_low:
    # You probably only want one return here, not two in a row
    # return "BULLISH" if condition met, else "RANGE"
    return "BULLISH"
else:
    return "RANGE"


# -------------------------
# LTF ENTRY (CONFIRMATION)
# -------------------------
def analyse_ltf_entry(candles, htf_bias):
    if len(candles) < 60:
        return None

    highs = [float(c["high"]) for c in candles]
    lows = [float(c["low"]) for c in candles]
    closes = [float(c["close"]) for c in candles]

    last_close = closes[-1]

    # --- Supply / Demand zones ---
    supply = max(highs[-30:-5])
    demand = min(lows[-30:-5])

    # --- CHOCH / BOS confirmation ---
    prev_high = max(highs[-10:-5])
    prev_low = min(lows[-10:-5])

    # BEARISH SETUP
    if htf_bias == "BEARISH":
        # price reacts at supply and breaks structure
        if last_close < prev_low and supply > last_close:
            entry = last_close
            sl = supply
            tp = entry - 2 * (sl - entry)

            return {
                "direction": "SELL",
                "bias": htf_bias,
                "entry": round(entry, 5),
                "sl": round(sl, 5),
                "tp": round(tp, 5),
                "reason": "LTF CHOCH/BOS after reaction from supply in HTF bearish context"
            }

    # BULLISH SETUP
    if htf_bias == "BULLISH":
        if last_close > prev_high and demand < last_close:
            entry = last_close
            sl = demand
            tp = entry + 2 * (entry - sl)

            return {
                "direction": "BUY",
                "bias": htf_bias,
                "entry": round(entry, 5),
                "sl": round(sl, 5),
                "tp": round(tp, 5),
                "reason": "LTF CHOCH/BOS after reaction from demand in HTF bullish context"
            }

    return Noneimport requests

# -------------------------
# HTF BIAS CHECK
# -------------------------
if recent_high > prev_high and recent_low > prev_low:
    # You probably only want one return here, not two in a row
    # return "BULLISH" if condition met, else "RANGE"
    return "BULLISH"
else:
    return "RANGE"


# -------------------------
# LTF ENTRY (CONFIRMATION)
# -------------------------
def analyse_ltf_entry(candles, htf_bias):
    if len(candles) < 60:
        return None

    highs = [float(c["high"]) for c in candles]
    lows = [float(c["low"]) for c in candles]
    closes = [float(c["close"]) for c in candles]

    last_close = closes[-1]

    # --- Supply / Demand zones ---
    supply = max(highs[-30:-5])
    demand = min(lows[-30:-5])

    # --- CHOCH / BOS confirmation ---
    prev_high = max(highs[-10:-5])
    prev_low = min(lows[-10:-5])

    # BEARISH SETUP
    if htf_bias == "BEARISH":
        # price reacts at supply and breaks structure
        if last_close < prev_low and supply > last_close:
            entry = last_close
            sl = supply
            tp = entry - 2 * (sl - entry)

            return {
                "direction": "SELL",
                "bias": htf_bias,
                "entry": round(entry, 5),
                "sl": round(sl, 5),
                "tp": round(tp, 5),
                "reason": "LTF CHOCH/BOS after reaction from supply in HTF bearish context"
            }

    # BULLISH SETUP
    if htf_bias == "BULLISH":
        if last_close > prev_high and demand < last_close:
            entry = last_close
            sl = demand
            tp = entry + 2 * (entry - sl)

            return {
                "direction": "BUY",
                "bias": htf_bias,
                "entry": round(entry, 5),
                "sl": round(sl, 5),
                "tp": round(tp, 5),
                "reason": "LTF CHOCH/BOS after reaction from demand in HTF bullish context"
            }

    return Noneimport requests

# -------------------------
# HTF BIAS CHECK
# -------------------------
if recent_high > prev_high and recent_low > prev_low:
    # You probably only want one return here, not two in a row
    # return "BULLISH" if condition met, else "RANGE"
    return "BULLISH"
else:
    return "RANGE"


# -------------------------
# LTF ENTRY (CONFIRMATION)
# -------------------------
def analyse_ltf_entry(candles, htf_bias):
    if len(candles) < 60:
        return None

    highs = [float(c["high"]) for c in candles]
    lows = [float(c["low"]) for c in candles]
    closes = [float(c["close"]) for c in candles]

    last_close = closes[-1]

    # --- Supply / Demand zones ---
    supply = max(highs[-30:-5])
    demand = min(lows[-30:-5])

    # --- CHOCH / BOS confirmation ---
    prev_high = max(highs[-10:-5])
    prev_low = min(lows[-10:-5])

    # BEARISH SETUP
    if htf_bias == "BEARISH":
        # price reacts at supply and breaks structure
        if last_close < prev_low and supply > last_close:
            entry = last_close
            sl = supply
            tp = entry - 2 * (sl - entry)

            return {
                "direction": "SELL",
                "bias": htf_bias,
                "entry": round(entry, 5),
                "sl": round(sl, 5),
                "tp": round(tp, 5),
                "reason": "LTF CHOCH/BOS after reaction from supply in HTF bearish context"
            }

    # BULLISH SETUP
    if htf_bias == "BULLISH":
        if last_close > prev_high and demand < last_close:
            entry = last_close
            sl = demand
            tp = entry + 2 * (entry - sl)

            return {
                "direction": "BUY",
                "bias": htf_bias,
                "entry": round(entry, 5),
                "sl": round(sl, 5),
                "tp": round(tp, 5),
                "reason": "LTF CHOCH/BOS after reaction from demand in HTF bullish context"
            }

    return Noneimport requests

# -------------------------
# HTF BIAS CHECK
# -------------------------
if recent_high > prev_high and recent_low > prev_low:
    # You probably only want one return here, not two in a row
    # return "BULLISH" if condition met, else "RANGE"
    return "BULLISH"
else:
    return "RANGE"


# -------------------------
# LTF ENTRY (CONFIRMATION)
# -------------------------
def analyse_ltf_entry(candles, htf_bias):
    if len(candles) < 60:
        return None

    highs = [float(c["high"]) for c in candles]
    lows = [float(c["low"]) for c in candles]
    closes = [float(c["close"]) for c in candles]

    last_close = closes[-1]

    # --- Supply / Demand zones ---
    supply = max(highs[-30:-5])
    demand = min(lows[-30:-5])

    # --- CHOCH / BOS confirmation ---
    prev_high = max(highs[-10:-5])
    prev_low = min(lows[-10:-5])

    # BEARISH SETUP
    if htf_bias == "BEARISH":
        # price reacts at supply and breaks structure
        if last_close < prev_low and supply > last_close:
            entry = last_close
            sl = supply
            tp = entry - 2 * (sl - entry)

            return {
                "direction": "SELL",
                "bias": htf_bias,
                "entry": round(entry, 5),
                "sl": round(sl, 5),
                "tp": round(tp, 5),
                "reason": "LTF CHOCH/BOS after reaction from supply in HTF bearish context"
            }

    # BULLISH SETUP
    if htf_bias == "BULLISH":
        if last_close > prev_high and demand < last_close:
            entry = last_close
            sl = demand
            tp = entry + 2 * (entry - sl)

            return {
                "direction": "BUY",
                "bias": htf_bias,
                "entry": round(entry, 5),
                "sl": round(sl, 5),
                "tp": round(tp, 5),
                "reason": "LTF CHOCH/BOS after reaction from demand in HTF bullish context"
            }

    return Noneimport requests

# -------------------------
# HTF BIAS CHECK
# -------------------------
if recent_high > prev_high and recent_low > prev_low:
    # You probably only want one return here, not two in a row
    # return "BULLISH" if condition met, else "RANGE"
    return "BULLISH"
else:
    return "RANGE"


# -------------------------
# LTF ENTRY (CONFIRMATION)
# -------------------------
def analyse_ltf_entry(candles, htf_bias):
    if len(candles) < 60:
        return None

    highs = [float(c["high"]) for c in candles]
    lows = [float(c["low"]) for c in candles]
    closes = [float(c["close"]) for c in candles]

    last_close = closes[-1]

    # --- Supply / Demand zones ---
    supply = max(highs[-30:-5])
    demand = min(lows[-30:-5])

    # --- CHOCH / BOS confirmation ---
    prev_high = max(highs[-10:-5])
    prev_low = min(lows[-10:-5])

    # BEARISH SETUP
    if htf_bias == "BEARISH":
        # price reacts at supply and breaks structure
        if last_close < prev_low and supply > last_close:
            entry = last_close
            sl = supply
            tp = entry - 2 * (sl - entry)

            return {
                "direction": "SELL",
                "bias": htf_bias,
                "entry": round(entry, 5),
                "sl": round(sl, 5),
                "tp": round(tp, 5),
                "reason": "LTF CHOCH/BOS after reaction from supply in HTF bearish context"
            }

    # BULLISH SETUP
    if htf_bias == "BULLISH":
        if last_close > prev_high and demand < last_close:
            entry = last_close
            sl = demand
            tp = entry + 2 * (entry - sl)

            return {
                "direction": "BUY",
                "bias": htf_bias,
                "entry": round(entry, 5),
                "sl": round(sl, 5),
                "tp": round(tp, 5),
                "reason": "LTF CHOCH/BOS after reaction from demand in HTF bullish context"
            }

    return None
