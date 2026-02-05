# market_data.py

import requests
from config import MARKET_API_KEY, SYMBOL, TIMEFRAME, CANDLE_LIMIT

def fetch_candles():
    url = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": SYMBOL,
        "interval": TIMEFRAME,
        "outputsize": CANDLE_LIMIT,
        "apikey": MARKET_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "values" not in data:
        return []

    candles = []
    for c in reversed(data["values"]):
        candles.append({
            "open": float(c["open"]),
            "high": float(c["high"]),
            "low": float(c["low"]),
            "close": float(c["close"])
        })

    return candles
