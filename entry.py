# entry.py
import requests
import pandas as pd
import time
from config import API_KEY, HTF, LTF, RR_RATIO

# Cache for HTF and LTF data
htf_cache = {}
ltf_cache = {}

def fetch_candles(symbol, interval, outputsize=100):
    """Fetch candles from TwelveData API with caching"""
    key = f"{symbol}_{interval}"
    now = time.time()
    # Check cache
    if key in htf_cache and interval == HTF:
        if now - htf_cache[key]['timestamp'] < 3600:  # 1h for HTF
            return htf_cache[key]['data']
    if key in ltf_cache and interval == LTF:
        if now - ltf_cache[key]['timestamp'] < 300:  # 5min for LTF
            return ltf_cache[key]['data']

    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval={interval}&outputsize={outputsize}&apikey={API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        if "values" not in data:
            print(f"No data returned for {symbol}")
            return None
        df = pd.DataFrame(data["values"])
        df = df[::-1]  # Oldest first
        df["close"] = df["close"].astype(float)
        df["high"] = df["high"].astype(float)
        df["low"] = df["low"].astype(float)
        # Save cache
        if interval == HTF:
            htf_cache[key] = {'data': df, 'timestamp': now}
        else:
            ltf_cache[key] = {'data': df, 'timestamp': now}
        return df
    except Exception as e:
        print(f"Error fetching candles for {symbol}: {e}")
        return None

def analyse_htf_structure(df):
    """Determine HTF bias and last high/low"""
    if df is None or len(df) < 3:
        return None, None, None
    prev_high = df['high'].iloc[-2]
    prev_low = df['low'].iloc[-2]
    last_close = df['close'].iloc[-1]

    if last_close > prev_high:
        bias = "BULLISH"
    elif last_close < prev_low:
        bias = "BEARISH"
    else:
        bias = "RANGE"
    return bias, prev_high, prev_low

def analyse_ltf_entry(symbol, htf_bias, htf_prev_high, htf_prev_low):
    """Check for LTF retest entries based on minimum conditions"""
    df = fetch_candles(symbol, LTF)
    if df is None:
        return None

    last_close = df['close'].iloc[-1]
    last_high = df['high'].iloc[-1]
    last_low = df['low'].iloc[-1]

    conditions_met = 0
    entry = None
    sl = None
    tp = None

    # Example conditions (you can expand)
    # 1. Candle closes above/below LTF high/low (CHoCH)
    if htf_bias == "BULLISH" and last_close > htf_prev_high:
        conditions_met += 1
    if htf_bias == "BEARISH" and last_close < htf_prev_low:
        conditions_met += 1

    # 2. Retest: price near previous swing
    if htf_bias == "BULLISH" and last_low <= htf_prev_low * 1.001:
        conditions_met += 1
    if htf_bias == "BEARISH" and last_high >= htf_prev_high * 0.999:
        conditions_met += 1

    # Add more conditions like support/resistance, supply/demand, order blocks...

    if conditions_met >= 2:  # minimum required
        # Set entry, SL, TP
        if htf_bias == "BULLISH":
            entry = last_close
            sl = htf_prev_low
            tp = entry + (entry - sl) * RR_RATIO
        elif htf_bias == "BEARISH":
            entry = last_close
            sl = htf_prev_high
            tp = entry - (sl - entry) * RR_RATIO
        return {"symbol": symbol, "entry": entry, "sl": sl, "tp": tp, "direction": htf_bias}

    return None
