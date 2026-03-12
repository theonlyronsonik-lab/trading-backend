# entry.py
import requests
import pandas as pd
import time

# -----------------------------
# CONFIG / GLOBALS
# -----------------------------
API_KEY = "d143e9bb8b0c4d7487872fd699280bde"  # set your API key here
API_LOOP_DELAY = 300  # seconds between API calls to avoid free plan limit
HTF_CACHE = {}  # cache for HTF candles to avoid repeated calls

# -----------------------------
# GET CANDLES
# -----------------------------
def get_candles(symbol, timeframe, limit=100):
    """
    Fetches OHLC candles from TwelveData. Returns DataFrame.
    """
    if timeframe in HTF_CACHE.get(symbol, {}):
        # use cached HTF candles if timeframe matches cached
        df, last_fetch_time = HTF_CACHE[symbol][timeframe]
        elapsed = time.time() - last_fetch_time
        # only fetch new HTF if elapsed >= timeframe in seconds
        tf_seconds = timeframe_to_seconds(timeframe)
        if elapsed < tf_seconds:
            return df

    url = f"https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbol,
        "interval": timeframe,
        "outputsize": limit,
        "apikey": API_KEY
    }

    try:
        r = requests.get(url, params=params)
        data = r.json()
        if "values" not in data:
            print(f"No data returned for {symbol} ({timeframe})")
            return pd.DataFrame()
        df = pd.DataFrame(data["values"])
        df = df[::-1]  # chronological order
        for col in ["open", "high", "low", "close"]:
            df[col] = df[col].astype(float)

        # Cache HTF candles
        if symbol not in HTF_CACHE:
            HTF_CACHE[symbol] = {}
        HTF_CACHE[symbol][timeframe] = (df, time.time())

        return df

    except Exception as e:
        print(f"TwelveData error for {symbol}: {e}")
        return pd.DataFrame()
    finally:
        time.sleep(API_LOOP_DELAY)

# -----------------------------
# HTF ANALYSIS
# -----------------------------
def analyse_htf_structure(df):
    """
    Determines HTF bias using HH/HL or LL/LH logic.
    Returns "BULLISH", "BEARISH", or "RANGE".
    """
    if df.empty or len(df) < 3:
        return "RANGE"

    highs = df['high']
    lows = df['low']
    closes = df['close']

    if closes.iloc[-1] > highs.iloc[-2]:
        return "BULLISH"
    elif closes.iloc[-1] < lows.iloc[-2]:
        return "BEARISH"
    else:
        return "RANGE"

# -----------------------------
# LTF ENTRY WITH RE-TEST
# -----------------------------
def analyse_ltf_entry(htf_bias, ltf_df, swing_low, swing_high, confirmations_needed=1):
    """
    Checks for retest entry within swing range with min 1 confirmations:
    - CHoCH/BOS
    - Support/Resistance
    - Supply/Demand
    """
    if ltf_df.empty:
        return None, None, None

    last_close = ltf_df['close'].iloc[-1]
    last_low = ltf_df['low'].iloc[-1]
    last_high = ltf_df['high'].iloc[-1]

    confirmations = 0

    # Supply/Demand zone confirmation (simple example)
    # Here you can replace with your supply/demand detection logic
    demand_zone = swing_low + (swing_high - swing_low) * 0.3
    supply_zone = swing_high - (swing_high - swing_low) * 0.3
    if htf_bias == "BULLISH" and last_low <= demand_zone:
        confirmations += 1
    elif htf_bias == "BEARISH" and last_high >= supply_zone:
        confirmations += 1

    # Only send entry if minimum confirmations met
    MIN_CONFIRMATIONS = confirmations_needed
    if confirmations < MIN_CONFIRMATIONS:
        return None, None, None

 

# -----------------------------
# UTILITY: TIMEFRAME TO SECONDS
# -----------------------------
def timeframe_to_seconds(tf):
    """
    Converts TwelveData timeframe string to seconds.
    """
    if tf.endswith("min"):
        return int(tf.replace("min", "")) * 60
    elif tf.endswith("h"):
        return int(tf.replace("h", "")) * 3600
    elif tf.endswith("D"):
        return
        int(tf.replace("D", "")) * 86400
    return 60  # default fallback
