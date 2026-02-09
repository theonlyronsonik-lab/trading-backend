import requests
import time
from config import TWELVE_API_KEY

BASE_URL = "https://api.twelvedata.com/time_series"

# Simple in-memory cache to reduce API calls
_cache = {}
CACHE_TTL = 60  # seconds


def get_candles(symbol, timeframe, limit=50):
    """
    Returns a list of candles:
    [
        {
            "datetime": str,
            "open": float,
            "high": float,
            "low": float,
            "close": float
        }
    ]
    """

    now = time.time()
    cache_key = f"{symbol}_{timeframe}_{limit}"

    if cache_key in _cache:
        data, timestamp = _cache[cache_key]
        if now - timestamp < CACHE_TTL:
            return data

    params = {
        "symbol": symbol,
        "interval": timeframe,
        "outputsize": limit,
        "apikey": TWELVE_API_KEY
    }

    response = requests.get(BASE_URL, params=params, timeout=10)
    data = response.json()

    if "values" not in data:
        raise Exception(f"TwelveData error: {data}")

    candles = []
    for c in reversed(data["values"]):
        candles.append({
            "datetime": c["datetime"],
            "open": float(c["open"]),
            "high": float(c["high"]),
            "low": float(c["low"]),
            "close": float(c["close"]),
        })

    _cache[cache_key] = (candles, now)
    return candles
