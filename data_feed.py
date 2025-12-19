import requests
from config import API_KEY, BASE_URL

def get_candles(symbol, timeframe, limit=200):
    url = f"{BASE_URL}/time_series"
    params = {
        "symbol": symbol,
        "interval": timeframe,
        "apikey": API_KEY,
        "outputsize": limit,
        "format": "JSON"
    }
    r = requests.get(url, params=params)
    data = r.json()

    if "values" not in data:
        return []

    candles = []
    for c in reversed(data["values"]):
        candles.append({
            "open": float(c["open"]),
            "high": float(c["high"]),
            "low": float(c["low"]),
            "close": float(c["close"]),
            "time": c["datetime"]
        })

    return candles
