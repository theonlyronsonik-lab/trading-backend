import os
import requests

API_KEY = os.getenv("TWELVEDATA_API_KEY")
SYMBOL = os.getenv("SYMBOL", "XAU/USD")
TIMEFRAME = os.getenv("TIMEFRAME", "15min")

def get_candles():
    url = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": SYMBOL,
        "interval": TIMEFRAME,
        "outputsize": 200,
        "apikey": API_KEY
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
