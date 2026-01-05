import requests

API_KEY = "YOUR_API_KEY_HERE"

def get_candles(symbol="XAUUSD", timeframe="1h", limit=100):
    url = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbol,
        "interval": timeframe,
        "apikey": API_KEY,
        "outputsize": limit
    }

    response = requests.get(url).json()

    if "values" not in response:
        return []

    candles = []
    for c in response["values"]:
        candles.append({
            "open": float(c["open"]),
            "high": float(c["high"]),
            "low": float(c["low"]),
            "close": float(c["close"])
        })

    return candles
