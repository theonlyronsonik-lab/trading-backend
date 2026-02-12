# structure.py

def find_swings(df):
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


def detect_bos(df, state):
    swing_high, swing_low = find_swings(df)

    if swing_high is None or swing_low is None:
        return

    last_close = df["close"].iloc[-1]

    if last_close > swing_high:
        state.direction = "bullish"
        state.range_low = swing_low
        state.range_high = swing_high
        state.trade_taken = False
        state.waiting_for_htf_retest = True
        state.waiting_for_choch = False
        identify_demand_zone(df, state)

    elif last_close < swing_low:
        state.direction = "bearish"
        state.range_low = swing_low
        state.range_high = swing_high
        state.trade_taken = False
        state.waiting_for_htf_retest = True
        state.waiting_for_choch = False
        identify_supply_zone(df, state)


def identify_demand_zone(df, state):
    for i in range(len(df)-2, 0, -1):
        candle = df.iloc[i]
        if candle["close"] < candle["open"]:
            state.demand_zone = (candle["low"], candle["open"])
            break


def identify_supply_zone(df, state):
    for i in range(len(df)-2, 0, -1):
        candle = df.iloc[i]
        if candle["close"] > candle["open"]:
            state.supply_zone = (candle["open"], candle["high"])
            break


def check_htf_retest(price, state):
    if not state.waiting_for_htf_retest:
        return False

    if state.direction == "bullish" and state.demand_zone:
        low, high = state.demand_zone
        if low <= price <= high:
            state.waiting_for_htf_retest = False
            state.waiting_for_choch = True
            return True

    if state.direction == "bearish" and state.supply_zone:
        low, high = state.supply_zone
        if low <= price <= high:
            state.waiting_for_htf_retest = False
            state.waiting_for_choch = True
            return True

    return False
