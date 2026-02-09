import requests
import time
from config import TWELVE_DATA_API_KEY, CANDLE_LIMIT

_cache = {}  # symbol_interval → last_timestamp, candles


def fetch_candles(symbol, interval):
    cache_key = f"{symbol}_{interval}"

    url = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbol,
        "interval": interval,
        "apikey": TWELVE_DATA_API_KEY,
        "outputsize": CANDLE_LIMIT,
        "format": "JSON"
    }

    response = requests.get(url, params=params, timeout=10)
    data = response.json()

    if data.get("status") == "error":
        print(f"No candle data for {symbol} ({interval})")
        print("Response:", data)
        return None

    candles = data.get("values", [])
    if not candles:
        return None

    latest_time = candles[0]["datetime"]

    # 🧠 CACHE CHECK
    if cache_key in _cache:
        last_time, cached = _cache[cache_key]
        if latest_time == last_time:
            return cached  # no new candle → no API burn

    _cache[cache_key] = (latest_time, candles)
    return candles
