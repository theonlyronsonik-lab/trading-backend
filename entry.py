# entry.py

def find_ltf_swings(df):
    swing_high = None
    swing_low = None

    for i in range(2, len(df) - 2):
        if (
            df["high"].iloc[i] > df["high"].iloc[i-1] and
            df["high"].iloc[i] > df["high"].iloc[i-2] and
            df["high"].iloc[i] > df["high"].iloc[i+1] and
            df["high"].iloc[i] > df["high"].iloc[i+2]
        ):
            swing_high = df["high"].iloc[i]

        if (
            df["low"].iloc[i] < df["low"].iloc[i-1] and
            df["low"].iloc[i] < df["low"].iloc[i-2] and
            df["low"].iloc[i] < df["low"].iloc[i+1] and
            df["low"].iloc[i] < df["low"].iloc[i+2]
        ):
            swing_low = df["low"].iloc[i]

    return swing_high, swing_low


def detect_choch(df, state):
    if not state.waiting_for_choch:
        return False

    swing_high, swing_low = find_ltf_swings(df)
    last_close = df["close"].iloc[-1]

    if state.direction == "bullish" and swing_high and last_close > swing_high:
        state.choch_level = swing_high
        return True

    if state.direction == "bearish" and swing_low and last_close < swing_low:
        state.choch_level = swing_low
        return True

    return False


def check_entry(df, state):
    if state.trade_taken:
        return None

    if state.choch_level is None:
        return None

    current = df.iloc[-1]
    price = current["close"]

    confirmations = 0

    # Confirmation 1: Retest of CHoCH level
    if state.direction == "bullish" and price <= state.choch_level:
        confirmations += 1

    if state.direction == "bearish" and price >= state.choch_level:
        confirmations += 1

    # Confirmation 2: Discount / Premium
    midpoint = (state.range_high + state.range_low) / 2

    if state.direction == "bullish" and price < midpoint:
        confirmations += 1

    if state.direction == "bearish" and price > midpoint:
        confirmations += 1

    # Confirmation 3: Strong candle
    if state.direction == "bullish" and current["close"] > current["open"]:
        confirmations += 1

    if state.direction == "bearish" and current["close"] < current["open"]:
        confirmations += 1

    if confirmations >= 2:
        sl, tp = calculate_sl_tp(price, state)
        state.trade_taken = True
        state.waiting_for_choch = False
        state.choch_level = None
        return {
            "direction": state.direction,
            "entry": price,
            "sl": sl,
            "tp": tp
        }

    return None


def calculate_sl_tp(price, state):
    if state.direction == "bullish":
        sl = state.range_low
        tp = state.range_high
    else:
        sl = state.range_high
        tp = state.range_low

    return sl, tp
